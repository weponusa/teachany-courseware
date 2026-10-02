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


  /* ---------- 5) 磁场：拖磁铁 → 吸引/排斥 + 磁力线（偶极场示意） ---------- */
  function magnet(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      initial: { ax: 210, ay: 220, bx: 600, by: 220, showField: true },
      cursor: 'grab',
      onPointer: function (type, p, s) {
        if (type === 'pointerdown') {
          s.drag = (Math.abs(p.x - s.ax) <= Math.abs(p.x - s.bx)) ? 'a' : 'b';
        }
        if (type === 'pointermove' && s.drag) {
          if (s.drag === 'a') { s.ax = Math.max(60, Math.min(380, p.x)); s.ay = Math.max(120, Math.min(330, p.y)); }
          else { s.bx = Math.max(420, Math.min(740, p.x)); s.by = Math.max(120, Math.min(330, p.y)); }
        }
        if (type === 'pointerup' || type === 'pointerleave') { s.drag = null; }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var MW = 34, MH = 108;                       // 两块磁铁等大：上 N 下 S
        function bar(x, y) {
          ctx.fillStyle = '#ef4444'; h.rrect(ctx, x - MW / 2, y - MH / 2, MW, MH / 2, 6); ctx.fill();
          ctx.fillStyle = '#3b82f6'; h.rrect(ctx, x - MW / 2, y, MW, MH / 2, 6); ctx.fill();
          h.label(ctx, 'N', x, y - MH / 4, '#fff', 15, 'center', '800');
          h.label(ctx, 'S', x, y + MH / 4, '#fff', 15, 'center', '800');
        }
        var d = Math.hypot(s.bx - s.ax, s.by - s.ay);
        var close = d < 230;
        // 磁力线：磁铁之间 4 条弧（由 N 出发弯向另一块的 S）
        if (s.showField) {
          ctx.strokeStyle = P.accent2; ctx.globalAlpha = close ? 0.75 : 0.5;
          for (var k = 0; k < 4; k++) {
            var t = (k + 1) / 5, bow = 46 + k * 40;
            ctx.lineWidth = 1.6;
            ctx.beginPath();
            ctx.moveTo(s.ax, s.ay - MH / 2);
            ctx.bezierCurveTo(s.ax + (s.bx - s.ax) * 0.35, s.ay - MH / 2 - bow,
              s.bx - (s.bx - s.ax) * 0.35, s.by - MH / 2 - bow, s.bx, s.by - MH / 2);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(s.ax, s.ay + MH / 2);
            ctx.bezierCurveTo(s.ax + (s.bx - s.ax) * 0.35, s.ay + MH / 2 + bow,
              s.bx - (s.bx - s.ax) * 0.35, s.by + MH / 2 + bow, s.bx, s.by + MH / 2);
            ctx.stroke();
          }
          ctx.globalAlpha = 1;
          h.label(ctx, '磁力线（示意）', W / 2, 20, P.accent2, 11.5, 'center', '600');
        }
        bar(s.ax, s.ay); bar(s.bx, s.by);
        // 距离参考线
        var my = Math.max(s.ay, s.by) + MH / 2 + 26;
        ctx.strokeStyle = P.grid; ctx.setLineDash([4, 4]); ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(s.ax, my); ctx.lineTo(s.bx, my); ctx.stroke(); ctx.setLineDash([]);
        h.label(ctx, '间距 ' + Math.round(d / 6) + ' cm', (s.ax + s.bx) / 2, my, P.muted, 12, 'center', '600');
        // 靠得近时提示相互作用（让学生自己判断吸引/排斥）
        if (close) {
          h.label(ctx, '很近了 —— 它们相互吸引还是排斥？', W / 2, H - 18, P.ink, 12.5, 'center', '700');
        } else {
          h.label(ctx, '拖动任一磁铁靠近另一块 →', W - 22, 20, P.muted, 12, 'right', '600');
        }
        this.readout('两块磁铁间距约 ' + Math.round(d / 6) + ' cm：让 N 极靠近 N 极观察排斥，N 极靠近 S 极观察吸引——磁极间的相互作用规律请自己试出来。');
      }
    });
  }

  /* ---------- 6) 月相 / 昼夜：公转位置 → 看到的月相 / 昼夜 ---------- */
  function moon(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      sliders: { ang: { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '公转位置 ' + v + '°'; } } },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var cx = W * 0.32, cy = H / 2, R = Math.min(W * 0.22, H * 0.34);
        // 地球
        ctx.beginPath(); ctx.arc(cx, cy, 30, 0, Math.PI * 2); ctx.fillStyle = P.accent; ctx.fill();
        h.label(ctx, '地球', cx, cy + 48, P.muted, 12, 'center', '600');
        // 轨道 + 月球
        ctx.strokeStyle = P.grid; ctx.setLineDash([5, 5]);
        ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]);
        var a = (s.ang || 0) * Math.PI / 180 - Math.PI / 2;
        var mx = cx + R * Math.cos(a), my = cy + R * Math.sin(a);
        ctx.beginPath(); ctx.arc(mx, my, 15, 0, Math.PI * 2); ctx.fillStyle = '#cbd5e1'; ctx.fill();
        // 太阳光方向：自左向右（示意）
        ctx.strokeStyle = P.accent2; ctx.lineWidth = 2;
        for (var i = 0; i < 4; i++) {
          var yy = 40 + i * 44;
          h.arrow(ctx, 18, yy, 78, yy, P.accent2, 2, 7);
        }
        h.label(ctx, '☀️ 太阳光', 20, 22, P.accent2, 12, 'left', '700');
        // 右半区：观察者看到的月相
        var ox = W * 0.72, oy = cy, r2 = 62;
        ctx.beginPath(); ctx.arc(ox, oy, r2, 0, Math.PI * 2); ctx.fillStyle = '#0f172a'; ctx.globalAlpha = 0.25; ctx.fill(); ctx.globalAlpha = 1;
        ctx.strokeStyle = P.grid; ctx.stroke();
        // 相位：角 0=新月, 90=上弦, 180=满月, 270=下弦
        var ph = ((s.ang || 0) % 360 + 360) % 360;
        ctx.save();
        ctx.beginPath(); ctx.arc(ox, oy, r2, 0, Math.PI * 2); ctx.clip();
        ctx.fillStyle = '#e2e8f0';
        if (ph <= 180) { ctx.beginPath(); ctx.rect(ox - r2, oy - r2, r2, r2 * 2); ctx.fill(); }
        else { ctx.beginPath(); ctx.rect(ox, oy - r2, r2, r2 * 2); ctx.fill(); }
        var k = Math.cos(ph * Math.PI / 180);
        ctx.beginPath();
        ctx.ellipse(ox, oy, Math.abs(k) * r2, r2, 0, 0, Math.PI * 2);
        ctx.fillStyle = k > 0 ? '#e2e8f0' : '#0f172a';
        ctx.globalAlpha = 0.85; ctx.fill(); ctx.globalAlpha = 1;
        ctx.restore();
        var name = ph < 22 || ph > 338 ? '新月（看不见月亮）' : ph < 68 ? '蛾眉月' : ph < 112 ? '上弦月（右半边亮）'
          : ph < 158 ? '盈凸月' : ph < 202 ? '满月（整轮都亮）' : ph < 248 ? '亏凸月' : ph < 292 ? '下弦月（左半边亮）' : '残月';
        h.label(ctx, '地球上看到的：' + name, ox, oy + r2 + 26, P.ink, 13, 'center', '700');
        this.readout('月球位置 ' + Math.round(ph) + '° → 地球上看到「' + name + '」。拖动滑块让月球绕地球转一整圈，观察月相怎样从新月经上弦到满月再回到新月。');
      }
    });
  }

  /* ---------- 7) 雷达图：可拖拽的多个维度（能力/材料对比） ---------- */
  function radar(cfg) {
    var dims = cfg.dims || ['维度1', '维度2', '维度3', '维度4', '维度5'];
    var vals = (cfg.values || [3, 4, 2, 5, 3]).slice();
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      initial: { vals: vals, unit: cfg.unit || '' },
      cursor: 'crosshair',
      onPointer: function (type, p, s) {
        if (type !== 'pointerdown' && type !== 'pointermove') return;
        if (type === 'pointermove' && !s.dragAxis) return;
        var f = this.fit();
        var W = f.W, H = f.H, cx = W / 2, cy = H / 2 + 6, R = Math.min(W, H) * 0.32;
        var n = s.vals.length;
        // 找最近的轴
        var best = -1, bd = 1e9;
        for (var i = 0; i < n; i++) {
          var a = -Math.PI / 2 + i * 2 * Math.PI / n;
          var ax = cx + R * Math.cos(a), ay = cy + R * Math.sin(a);
          var d = Math.hypot(p.x - ax, p.y - ay);
          if (d < bd) { bd = d; best = i; }
        }
        if (type === 'pointerdown') { s.dragAxis = best; }
        if (best >= 0 && bd < 200) {
          var aa = -Math.PI / 2 + best * 2 * Math.PI / n;
          var proj = (p.x - cx) * Math.cos(aa) + (p.y - cy) * Math.sin(aa);
          var v = Math.max(1, Math.min(5, Math.round(proj / R * 5)));
          s.vals[best] = v;
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var cx = W / 2, cy = H / 2 + 6, R = Math.min(W, H) * 0.32, n = s.vals.length;
        // 网格
        ctx.strokeStyle = P.grid; ctx.lineWidth = 1;
        for (var ring = 1; ring <= 5; ring++) {
          ctx.beginPath();
          for (var i = 0; i <= n; i++) {
            var a = -Math.PI / 2 + i * 2 * Math.PI / n;
            var x = cx + (R * ring / 5) * Math.cos(a), y = cy + (R * ring / 5) * Math.sin(a);
            i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
          }
          ctx.stroke();
        }
        for (var j = 0; j < n; j++) {
          var aj = -Math.PI / 2 + j * 2 * Math.PI / n;
          ctx.beginPath(); ctx.moveTo(cx, cy);
          ctx.lineTo(cx + R * Math.cos(aj), cy + R * Math.sin(aj)); ctx.stroke();
          var lx = cx + (R + 26) * Math.cos(aj), ly = cy + (R + 26) * Math.sin(aj);
          h.label(ctx, dims[j], lx, ly, P.ink, 12.5, 'center', '700');
        }
        // 数据多边形
        ctx.beginPath();
        for (var q = 0; q <= n; q++) {
          var idx = q % n, aq = -Math.PI / 2 + idx * 2 * Math.PI / n, rq = R * s.vals[idx] / 5;
          var qx = cx + rq * Math.cos(aq), qy = cy + rq * Math.sin(aq);
          q ? ctx.lineTo(qx, qy) : ctx.moveTo(qx, qy);
        }
        ctx.closePath();
        ctx.fillStyle = P.fill; ctx.fill();
        ctx.strokeStyle = P.accent; ctx.lineWidth = 2.6; ctx.stroke();
        s.vals.forEach(function (v, i2) {
          var ai = -Math.PI / 2 + i2 * 2 * Math.PI / n, rr = R * v / 5;
          ctx.beginPath(); ctx.arc(cx + rr * Math.cos(ai), cy + rr * Math.sin(ai), 5, 0, Math.PI * 2);
          ctx.fillStyle = P.accent; ctx.fill();
        });
        h.label(ctx, '👆 拖动顶点调整各维度（1–5 分）', W / 2, H - 16, P.muted, 12, 'center', '600');
        this.readout((cfg.readoutText ? cfg.readoutText(s.vals) : dims.map(function (d3, i3) { return d3 + ' ' + s.vals[i3]; }).join('｜')) + '　—— 拖动顶点改变评分，雷达圈越大说明该方面越突出。');
      }
    });
  }

  /* ---------- 8) 配对/分类：点击左侧项 → 点右侧目标 ---------- */
  function match(cfg) {
    var items = cfg.items || [];
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      initial: { sel: null, done: {}, wrong: null },
      cursor: 'pointer',
      onPointer: function (type, p, s) {
        if (type !== 'pointerdown') return;
        var f = this.fit(), W = f.W, H = f.H;
        var n = items.length, rowH = Math.min(60, (H - 90) / n);
        for (var i = 0; i < n; i++) {
          var y = 56 + i * rowH;
          if (p.x < W * 0.5 && p.y > y - rowH / 2 && p.y < y + rowH / 2) { s.sel = i; s.wrong = null; return; }
          if (p.x > W * 0.5 && p.y > y - rowH / 2 && p.y < y + rowH / 2) {
            if (s.sel == null) return;
            if (items[s.sel].answer === i) { s.done[s.sel] = true; s.sel = null; }
            else { s.wrong = i; }
            return;
          }
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var n = items.length, rowH = Math.min(60, (H - 90) / n);
        h.label(ctx, '左边：感官／对象', W * 0.25, 26, P.muted, 12.5, 'center', '700');
        h.label(ctx, '右边：对应的功能／用途', W * 0.75, 26, P.muted, 12.5, 'center', '700');
        var rights = items.map(function (it, i) { return { t: it.right, i: i }; });
        rights.sort(function (a, b) { return a.t.length - b.t.length; });
        items.forEach(function (it, i) {
          var y = 56 + i * rowH;
          var ok = !!s.done[i];
          ctx.fillStyle = s.sel === i ? P.fill : (ok ? 'rgba(5,150,105,.12)' : 'rgba(148,163,184,.12)');
          ctx.strokeStyle = s.sel === i ? P.accent : (ok ? P.ok : P.grid);
          ctx.lineWidth = 2;
          h.rrect(ctx, W * 0.06, y - rowH * 0.34, W * 0.38, rowH * 0.68, 10); ctx.fill(); ctx.stroke();
          h.label(ctx, it.label + (ok ? '  ✓' : ''), W * 0.25, y, P.ink, 13.5, 'center', '700');
        });
        rights.forEach(function (r2, k) {
          var y = 56 + k * rowH;
          ctx.fillStyle = 'rgba(148,163,184,.12)'; ctx.strokeStyle = P.grid;
          h.rrect(ctx, W * 0.56, y - rowH * 0.34, W * 0.38, rowH * 0.68, 10); ctx.fill(); ctx.stroke();
          h.label(ctx, r2.t, W * 0.75, y, P.ink, 13.5, 'center', '600');
        });
        var total = items.length, got = Object.keys(s.done).length;
        this.readout('已完成 ' + got + ' / ' + total + (s.wrong != null ? '　刚才这一对不匹配，再换一个试试。' : '　先点左边一项，再点右边对应的目标。'));
      }
    });
  }


  /* ---------- 9) 通用「可点击结构图」：图形与热区都是数据（便于逐课填内容） ---------- */
  /* 支持形状：ellipse / rect / poly / line / text；热区：{name, info, x, y, r, tip} */
  function drawShape(ctx, P, sh) {
    ctx.save();
    if (sh.dash) { ctx.setLineDash(sh.dash); }
    if (sh.t === 'ellipse') {
      ctx.beginPath(); ctx.ellipse(sh.x, sh.y, sh.rx, sh.ry, sh.rot || 0, 0, Math.PI * 2);
      if (sh.fill) { ctx.fillStyle = sh.fill; ctx.fill(); }
      if (sh.stroke) { ctx.strokeStyle = sh.stroke; ctx.lineWidth = sh.w || 2; ctx.stroke(); }
    } else if (sh.t === 'rect') {
      ctx.beginPath();
      if (sh.r) { global.TeachAnyLab.helpers.rrect(ctx, sh.x, sh.y, sh.w2, sh.h2, sh.r); }
      else { ctx.rect(sh.x, sh.y, sh.w2, sh.h2); }
      if (sh.fill) { ctx.fillStyle = sh.fill; ctx.fill(); }
      if (sh.stroke) { ctx.strokeStyle = sh.stroke; ctx.lineWidth = sh.w || 2; ctx.stroke(); }
    } else if (sh.t === 'poly') {
      ctx.beginPath();
      (sh.pts || []).forEach(function (pt, i) { i ? ctx.lineTo(pt[0], pt[1]) : ctx.moveTo(pt[0], pt[1]); });
      ctx.closePath();
      if (sh.fill) { ctx.fillStyle = sh.fill; ctx.fill(); }
      if (sh.stroke) { ctx.strokeStyle = sh.stroke; ctx.lineWidth = sh.w || 2; ctx.stroke(); }
    } else if (sh.t === 'line') {
      ctx.beginPath(); ctx.moveTo(sh.x1, sh.y1); ctx.lineTo(sh.x2, sh.y2);
      ctx.strokeStyle = sh.color || P.grid; ctx.lineWidth = sh.w || 1.4; ctx.stroke();
    } else if (sh.t === 'text') {
      ctx.fillStyle = sh.color || P.ink;
      ctx.font = (sh.weight || '600') + ' ' + (sh.size || 12.5) + "px 'PingFang SC', system-ui, sans-serif";
      ctx.textAlign = sh.align || 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(sh.t2, sh.x, sh.y);
    }
    ctx.restore();
  }

  function parts(cfg) {
    var bg = cfg.bg || [], pts = cfg.parts || [];
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'pointer',
      initial: { sel: null, hover: null },
      onPointer: function (type, p, s) {
        var best = null, bd = 1e9;
        pts.forEach(function (it, i) {
          var d = Math.hypot(p.x - it.x, p.y - it.y);
          if (d < (it.r || 46) && d < bd) { bd = d; best = i; }
        });
        if (type === 'pointermove') { s.hover = best; }
        if (type === 'pointerdown' && best != null) { s.sel = best; }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        bg.forEach(function (sh) { drawShape(ctx, P, sh); });
        // 热区
        pts.forEach(function (it, i) {
          var on = (s.sel === i), hov = (s.hover === i);
          if (on || hov) {
            ctx.beginPath(); ctx.arc(it.x, it.y, (it.r || 46) * 0.96, 0, Math.PI * 2);
            ctx.fillStyle = on ? 'rgba(2,132,199,.18)' : 'rgba(2,132,199,.09)';
            ctx.fill();
            ctx.strokeStyle = P.accent; ctx.lineWidth = on ? 2.6 : 1.6; ctx.stroke();
          }
          ctx.beginPath(); ctx.arc(it.x, it.y, on ? 7 : 5, 0, Math.PI * 2);
          ctx.fillStyle = on ? P.accent : P.muted; ctx.fill();
          // 引线 + 名称
          var lx = it.lx != null ? it.lx : it.x, ly = it.ly != null ? it.ly : it.y - 42;
          ctx.strokeStyle = on ? P.accent : P.grid; ctx.lineWidth = 1.2;
          ctx.beginPath(); ctx.moveTo(it.x, it.y); ctx.lineTo(lx, ly + 10); ctx.stroke();
          h.label(ctx, it.name, lx, ly, on ? P.accent : P.ink, 12.5, it.align || 'center', on ? '800' : '700');
        });
        h.label(ctx, cfg.tip || '👆 点击图中的结构，查看名称与功能', W / 2, H - 16, P.muted, 12, 'center', '600');
        var cur = s.sel != null ? pts[s.sel] : (s.hover != null ? pts[s.hover] : null);
        if (cur) { this.readout((cur.name + '：' + (cur.info || '')) + (cur.tip ? '（' + cur.tip + '）' : '')); }
        else { this.readout(cfg.hint || '点击图中的圆点结构，查看它的名称与功能说明。'); }
      }
    });
  }


  /* ---------- 10) 饼图：可点击扇区（水分布等） ---------- */
  function pie(cfg) {
    var segs = cfg.segs || [];
    var total = segs.reduce(function (a, b) { return a + b.v; }, 0) || 1;
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'pointer',
      initial: { sel: null, hover: null }, sharedState: cfg.sharedState,
      onPointer: function (type, p, s) {
        var f = this.fit(), cx = f.W / 2 - 90, cy = f.H / 2, R = Math.min(f.W, f.H) * 0.34;
        var dx = p.x - cx, dy = p.y - cy, d = Math.hypot(dx, dy);
        var a0 = -Math.PI / 2, hit = null;
        if (d <= R) {
          var ang = Math.atan2(dy, dx);
          var acc = a0;
          for (var i = 0; i < segs.length; i++) {
            var sweep = 2 * Math.PI * segs[i].v / total;
            var a1 = acc + sweep;
            var aa = ang; while (aa < acc) aa += 2 * Math.PI;
            if (aa >= acc && aa < a1) { hit = i; break; }
            acc = a1;
          }
        }
        if (type === 'pointermove') { s.hover = hit; }
        if (type === 'pointerdown') { s.sel = hit; }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var cx = W / 2 - 90, cy = H / 2, R = Math.min(W, H) * 0.34, a0 = -Math.PI / 2;
        segs.forEach(function (sg, i) {
          var sweep = 2 * Math.PI * sg.v / total;
          ctx.beginPath(); ctx.moveTo(cx, cy);
          ctx.arc(cx, cy, (s.sel === i || s.hover === i) ? R * 1.04 : R, a0, a0 + sweep);
          ctx.closePath();
          ctx.fillStyle = sg.color; ctx.globalAlpha = (s.sel === i) ? 1 : 0.9; ctx.fill(); ctx.globalAlpha = 1;
          ctx.strokeStyle = P.bg; ctx.lineWidth = 2; ctx.stroke();
          if (sg.v / total > 0.05) {
            var mid = a0 + sweep / 2;
            h.label(ctx, Math.round(sg.v / total * 100) + '%', cx + R * 0.62 * Math.cos(mid), cy + R * 0.62 * Math.sin(mid), '#fff', 13, 'center', '800');
          }
          a0 += sweep;
        });
        // 图例
        var ly = cy - segs.length * 16;
        segs.forEach(function (sg, i) {
          ctx.fillStyle = sg.color;
          h.rrect(ctx, W - 200, ly + i * 32 - 8, 16, 16, 4); ctx.fill();
          h.label(ctx, sg.name, W - 176, ly + i * 32, (s.sel === i) ? P.accent : P.ink, 12.5, 'left', '700');
        });
        var cur = s.sel != null ? segs[s.sel] : null;
        this.readout(cur ? (cur.name + '：占' + (cur.v / total * 100).toFixed(1) + '%　' + cur.info)
                         : (cfg.hint || '👆 点击饼图的扇区，看这部分水在哪里、有多少。'));
      }
    });
  }

  /* ---------- 11) 尺子：拖动物体对齐 0 刻度 → 读数 ---------- */
  function ruler(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'grab',
      initial: { x: 60, dragging: false }, sharedState: cfg.sharedState,
      onPointer: function (type, p, s) {
        if (type === 'pointerdown') { s.dragging = true; }
        if (type === 'pointerup' || type === 'pointerleave') { s.dragging = false; }
        if (s.dragging && type === 'pointermove') {
          var f = this.fit();
          s.x = Math.max(-40, Math.min(f.W - 260, p.x - 60));
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var top = 40, mm = cfg.pxPerCm || 60;           // 1 cm = 60 px
        // 尺身
        ctx.fillStyle = cfg.dark ? 'rgba(226,232,240,.12)' : 'rgba(251,191,36,.25)';
        h.rrect(ctx, 20, top + 44, W - 40, 74, 8); ctx.fill();
        ctx.strokeStyle = P.grid; ctx.lineWidth = 1.5;
        h.rrect(ctx, 20, top + 44, W - 40, 74, 8); ctx.stroke();
        for (var c = 0; c * mm <= W - 70; c++) {
          var x = 30 + c * mm;
          ctx.strokeStyle = P.ink; ctx.lineWidth = 1.6;
          ctx.beginPath(); ctx.moveTo(x, top + 46); ctx.lineTo(x, top + 46 + (c % 5 === 0 ? 26 : (c % 1 === 0 ? 16 : 8))); ctx.stroke();
          if (c % 5 === 0) h.label(ctx, String(c / 5), x, top + 44 - 12, P.muted, 11.5, 'center', '600');
        }
        h.label(ctx, '单位：厘米（cm）', W - 40, top + 24, P.muted, 12, 'right', '600');
        // 被测物体（矩形，长度 3.4 cm）
        var ow = 3.4 * mm, ox = 30 + s.x, oy = top + 44 - 34;
        ctx.fillStyle = P.accent; ctx.globalAlpha = 0.85;
        h.rrect(ctx, ox, oy, ow, 30, 6); ctx.fill(); ctx.globalAlpha = 1;
        ctx.strokeStyle = P.accent; ctx.lineWidth = 2; h.rrect(ctx, ox, oy, ow, 30, 6); ctx.stroke();
        h.label(ctx, '👆 拖动我', ox + ow / 2, oy - 12, P.accent, 12, 'center', '700');
        // 0 刻度对齐提示
        var aligned = Math.abs(ox - 30) < 6;
        if (aligned) {
          ctx.strokeStyle = P.ok; ctx.lineWidth = 2; ctx.setLineDash([4, 4]);
          ctx.beginPath(); ctx.moveTo(30, oy - 6); ctx.lineTo(30, top + 120); ctx.stroke(); ctx.setLineDash([]);
        }
        this.readout(aligned
          ? '✓ 左端已对准 0 刻度：物体长 ' + (ow / mm).toFixed(1) + ' cm（读数时视线要与刻度垂直，减少误差）'
          : '把物体左端拖到 0 刻度线再读数 —— 现在左端没有对齐，直接读数会有误差。');
      }
    });
  }

  /* ---------- 12b) 三种传热方式：传导 / 对流 / 辐射（页面按钮 setMode 驱动） ---------- */
  function heatModes(cfg) {
    var shared = cfg.sharedState || { t: 0, running: true, mode: 'conduction', tt: 0 };
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, sharedState: shared,
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        s.tt = (s.tt || 0) + 1 / 60;
        var mode = s.mode || 'conduction';
        if (mode === 'conduction') {
          var x0 = 120, y0 = H / 2 - 22, len = W - 240, hh = 44;
          ctx.fillStyle = 'rgba(148,163,184,.5)'; h.rrect(ctx, x0, y0, len, hh, 8); ctx.fill();
          var front = Math.min(len, (s.tt * 90) % (len + 60));
          ctx.fillStyle = 'rgba(239,68,68,.75)'; h.rrect(ctx, x0, y0, front, hh, 8); ctx.fill();
          ctx.fillStyle = P.accent2; h.rrect(ctx, x0 - 26, y0 - 8, 26, hh + 16, 6); ctx.fill();
          h.label(ctx, '🔥 加热', x0 - 12, y0 - 26, P.accent2, 12.5, 'center', '700');
          h.label(ctx, '金属棒（固体）', W / 2, y0 - 30, P.ink, 13, 'center', '700');
          h.label(ctx, '热量沿金属棒从高温端传到低温端', W / 2, H - 42, P.bad, 13, 'center', '700');
          this.readout('热传导：热量沿着物体（这里是金属棒）从温度高的部分传到温度低的部分。金属是热的良导体——靠的是分子/自由电子的碰撞传递。');
        } else if (mode === 'convection') {
          var cx = W / 2, cy = H / 2, rw = 260, rh = 110;
          ctx.fillStyle = 'rgba(96,165,250,.18)'; h.rrect(ctx, cx - rw / 2, cy - rh / 2, rw, rh, 14); ctx.fill();
          ctx.strokeStyle = P.grid; ctx.lineWidth = 2; h.rrect(ctx, cx - rw / 2, cy - rh / 2, rw, rh, 14); ctx.stroke();
          ctx.fillStyle = P.accent2; h.rrect(ctx, cx - 110, cy + rh / 2 - 6, 220, 10, 5); ctx.fill();
          h.label(ctx, '🔥 从底部加热（水）', cx - 110, cy + rh / 2 + 26, P.accent2, 12.5, 'center', '700');
          for (var i = 0; i < 8; i++) {
            var ph = s.tt * 1.6 + i * 0.8;
            var rx = cx + Math.cos(ph) * 78, ry = cy + Math.sin(ph * 2) * 32;
            ctx.beginPath(); ctx.arc(rx, ry, 5, 0, Math.PI * 2);
            ctx.fillStyle = Math.sin(ph) > 0 ? '#ef4444' : '#60a5fa'; ctx.fill();
          }
          h.label(ctx, '热水上升 → 冷水下沉 → 形成环流', cx, cy - rh / 2 - 26, P.ink, 13, 'center', '700');
          this.readout('热对流：液体（或气体）受热后体积变大、密度变小而上升，冷的部分下沉补充，形成环流，把热量带到各处。');
        } else {
          var sx = 110, sy = 90, ex = W - 140, ey = H / 2;
          ctx.beginPath(); ctx.arc(sx, sy, 42, 0, Math.PI * 2); ctx.fillStyle = P.accent2; ctx.fill();
          h.label(ctx, '☀️ 太阳', sx, sy - 60, P.accent2, 13, 'center', '700');
          ctx.beginPath(); ctx.arc(ex, ey, 46, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(96,165,250,.5)'; ctx.fill();
          h.label(ctx, '地球', ex, ey + 70, P.ink, 13, 'center', '700');
          for (var k = 0; k < 5; k++) {
            var off = ((s.tt * 120 + k * 40) % 200);
            h.arrow(ctx, sx + 50 + off, sy + 30 + k * 18, sx + 112 + off, sy + 30 + k * 18, P.bad, 2.2);
          }
          h.label(ctx, '不需要介质，热量直接“辐射”过来', W / 2, H - 42, P.bad, 13, 'center', '700');
          this.readout('热辐射：物体以电磁波的形式向外辐射热量，不需要介质——所以日地之间的真空里，太阳的热也能传到地球。');
        }
        h.label(ctx, '当前方式：' + (mode === 'conduction' ? '热传导' : mode === 'convection' ? '热对流' : '热辐射'),
          W - 24, 24, P.accent, 12.5, 'right', '700');
      }
    });
  }

  /* ---------- 12) 热传递：两物体温度随时间趋于相同 ---------- */
  function heat(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      sliders: { k: { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '导热性能 ' + v; } } },
      initial: { t: 0, hot: 90, cold: 20, running: false }, sharedState: cfg.sharedState,
      buttons: { start: cfg.btnStart, reset: cfg.btnReset },
      onButton: function (name, s) {
        if (name === 'start') { s.running = true; }
        if (name === 'reset') { s.running = false; s.hot = 90; s.cold = 20; s.t = 0; }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var k = (typeof s.k === 'number') ? s.k : 5;
        if (s.running && Math.abs(s.hot - s.cold) > 0.2) {
          var rate = k * 0.004;
          var d = (s.hot - s.cold) * rate;
          s.hot -= d; s.cold += d; s.t += 1 / 60;
        }
        // 两个物体
        var bw = 150, bh = 110;
        function box(x, y, temp, color) {
          ctx.fillStyle = color; h.rrect(ctx, x, y, bw, bh, 12); ctx.fill();
          h.label(ctx, Math.round(temp) + ' ℃', x + bw / 2, y + bh / 2, '#fff', 17, 'center', '800');
        }
        box(90, 60, s.hot, 'rgba(239,68,68,.85)');
        box(W - 240, 60, s.cold, 'rgba(96,165,250,.85)');
        h.label(ctx, '热水/热物体', 90 + bw / 2, 44, P.accent2, 12.5, 'center', '700');
        h.label(ctx, '冷水/冷物体', W - 240 + bw / 2, 44, P.accent, 12.5, 'center', '700');
        // 热流箭头
        var diff = s.hot - s.cold;
        if (Math.abs(diff) > 0.5) {
          for (var i = 0; i < 3; i++) {
            var y = 84 + i * 30;
            h.arrow(ctx, 260, y, W - 262, y, P.bad, 2.4);
          }
          h.label(ctx, '热量从高温物体传给低温物体（热传递）', W / 2, 210, P.bad, 13, 'center', '700');
        } else {
          h.label(ctx, '✓ 温度相同了 —— 达到热平衡，热传递停止', W / 2, 210, P.ok, 13.5, 'center', '800');
        }
        h.label(ctx, '已用时间 ' + s.t.toFixed(1) + ' s', W / 2, 250, P.muted, 12, 'center', '600');
        this.readout(s.running
          ? (Math.abs(diff) > 0.5 ? '热量正在从热的传给冷的：温差 ' + Math.abs(diff).toFixed(1) + ' ℃。导热性能越强，温度趋近越快。'
                                  : '温度相同了，热传递停止（热平衡）——热传递的条件是存在温度差。')
          : '点击「开始传热」，观察两个物体温度怎样变化。热传递的方向永远是：高温 → 低温。');
      }
    });
  }

  function dissolveChips(W, H) {
    return { t: { x: W - 300, y: 42, w: 140 }, s: { x: W - 150, y: 42, w: 120 } };
  }

  /* ---------- 13) 溶解：物质/温度/搅拌 → 溶解快慢 ---------- */
  function dissolve(cfg) {
    var subs = cfg.subs || [{ n: '食盐', k: 1 }, { n: '白糖', k: 0.7 }, { n: '小苏打', k: 0.5 }, { n: '沙子', k: 0 }];
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'pointer',
      sliders: {
        temp: { el: cfg.sliderTemp, out: cfg.outTemp, fmt: function (v) { return v + ' ℃'; } },
        stir: { el: cfg.sliderStir, out: cfg.outStir, fmt: function (v) { return v ? '搅拌中' : '不搅拌'; } }
      },
      initial: { sel: 0, running: false, pcm: 0, t: 0 }, sharedState: cfg.sharedState,
      buttons: { start: cfg.btnStart, reset: cfg.btnReset },
      onButton: function (name, s) {
        if (name === 'start') { s.running = true; s.pcm = 0; s.t = 0; }
        if (name === 'reset') { s.running = false; s.pcm = 0; s.t = 0; }
      },
      onPointer: function (type, p, s) {
        if (type !== 'pointerdown') return;
        var f = this.fit(), n = subs.length, w = (f.W - 80) / n;
        for (var i = 0; i < n; i++) {
          if (p.x > 40 + i * w && p.x < 40 + (i + 1) * w && p.y > f.H - 70) { s.sel = i; s.pcm = 0; s.running = false; return; }
        }
        // 画布内控件：温度（20/40/60/80℃ 循环）与 搅拌（开/关）
        var chips = dissolveChips(f.W, f.H);
        if (p.y > chips.t.y - 16 && p.y < chips.t.y + 16 && p.x > chips.t.x && p.x < chips.t.x + chips.t.w) {
          s.temp = ((s.temp || 20) + 20); if (s.temp > 80) s.temp = 20; return;
        }
        if (p.y > chips.s.y - 16 && p.y < chips.s.y + 16 && p.x > chips.s.x && p.x < chips.s.x + chips.s.w) {
          s.stir = s.stir ? 0 : 1; return;
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var sub = subs[s.sel], kk = sub.k;
        var temp = (typeof s.temp === 'number') ? s.temp : 20;
        var stir = (typeof s.stir === 'number') ? s.stir : 0;
        var speed = kk * (0.6 + (temp - 20) / 60) * (stir ? 1.8 : 1);
        if (s.running && kk > 0) { s.pcm = Math.min(1, s.pcm + speed * 0.006); s.t += 1 / 60; }
        // 烧杯
        var bx = 200, by = 60, bw = 320, bh = 200;
        ctx.strokeStyle = P.grid; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(bx, by + bh); ctx.lineTo(bx + bw, by + bh); ctx.lineTo(bx + bw, by); ctx.stroke();
        ctx.fillStyle = 'rgba(96,165,250,.22)'; ctx.fillRect(bx + 2, by + 60, bw - 4, bh - 62);
        // 水分子/颗粒
        var N = 60, seed = 99;
        for (var i = 0; i < N; i++) {
          seed = (seed * 16807) % 2147483647;
          var u = seed / 2147483647;
          seed = (seed * 16807) % 2147483647;
          var v = seed / 2147483647;
          var remain = (i / N) > s.pcm;               // 未溶解的颗粒
          var px = bx + 12 + u * (bw - 24);
          var py = remain ? (by + bh - 16 - (1 - s.pcm) * 70 - v * 6)
                          : (by + 70 + v * (bh - 90) + (stir ? Math.sin(s.t * 4 + i) * 10 : 0));
          ctx.beginPath(); ctx.arc(px, py, remain ? 4 : 2.6, 0, Math.PI * 2);
          ctx.fillStyle = remain ? (kk === 0 ? '#a16207' : '#e2e8f0') : 'rgba(226,232,240,.65)';
          ctx.fill();
        }
        h.label(ctx, sub.n, bx + bw / 2, by - 16, P.ink, 15, 'center', '800');
        // 画布内控件：温度 / 搅拌
        var chips = dissolveChips(W, H);
        [['🌡 温度 ' + temp + '℃', chips.t], [stir ? '🥄 搅拌中' : '🥄 不搅拌', chips.s]].forEach(function (c) {
          ctx.fillStyle = 'rgba(96,165,250,.16)'; ctx.strokeStyle = P.accent; ctx.lineWidth = 1.6;
          h.rrect(ctx, c[1].x, c[1].y - 16, c[1].w, 32, 8); ctx.fill(); ctx.stroke();
          h.label(ctx, c[0], c[1].x + c[1].w / 2, c[1].y, P.accent, 12.5, 'center', '700');
        });
        // 底部物质选择
        var n = subs.length, wcard = (W - 80) / n;
        subs.forEach(function (sb, i) {
          var x = 40 + i * wcard;
          ctx.fillStyle = s.sel === i ? P.fill : 'rgba(148,163,184,.14)';
          ctx.strokeStyle = s.sel === i ? P.accent : P.grid; ctx.lineWidth = 2;
          h.rrect(ctx, x + 6, H - 64, wcard - 12, 48, 10); ctx.fill(); ctx.stroke();
          h.label(ctx, sb.n, x + wcard / 2, H - 40, P.ink, 13, 'center', '700');
        });
        this.readout(kk === 0
          ? sub.n + ' 不溶于水：无论加热还是搅拌，它都不会溶解（这是“溶解能力”的差别，不是快慢问题）。'
          : (s.pcm >= 1 ? sub.n + ' 完全溶解了（用时 ' + s.t.toFixed(1) + ' s）：' + (stir ? '搅拌' : '不搅拌') + '、' + temp + '℃。'
                        : sub.n + ' 溶解中… 温度越高、越搅拌，溶解得越快（' + temp + '℃、' + (stir ? '搅拌' : '不搅拌') + '）。'));
      }
    });
  }

  function buildingChips(W, H) {
    return [{ x: 20, y: H - 34, w: 150 }, { x: 180, y: H - 34, w: 150 }, { x: 340, y: H - 34, w: 120 }];
  }

  /* ---------- 14) 绿色建筑：参数 → 能耗评分 ---------- */
  function building(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout,
      sliders: {
        insul: { el: cfg.sliderInsul, out: cfg.outInsul, fmt: function (v) { return v + ' 级'; } },
        solar: { el: cfg.sliderSolar, out: cfg.outSolar, fmt: function (v) { return v + ' 块'; } },
        green: { el: cfg.sliderGreen, out: cfg.outGreen, fmt: function (v) { return v + ' 处'; } }
      },
      sharedState: cfg.sharedState, cursor: 'pointer',
      onPointer: function (type, p, s) {
        if (type !== 'pointerdown') return;
        var f = this.fit();
        var chips = buildingChips(f.W, f.H);
        ['insul', 'solar', 'green'].forEach(function (key, i) {
          var c = chips[i];
          if (p.x > c.x && p.x < c.x + c.w && p.y > c.y - 18 && p.y < c.y + 18) {
            var max = key === 'insul' ? 5 : (key === 'solar' ? 6 : 4);
            s[key] = ((s[key] || 0) + 1); if (s[key] > max) s[key] = key === 'insul' ? 1 : 0;
          }
        });
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var insul = s.insul || 1, solar = s.solar || 0, green = s.green || 0;
        // 画布内控件
        { var chips = buildingChips(W, H);
          [['🧱 保温 ' + insul + ' 级', chips[0]], ['☀️ 太阳能板 ' + solar, chips[1]], ['🌳 绿化 ' + green, chips[2]]].forEach(function (c) {
            ctx.fillStyle = 'rgba(96,165,250,.16)'; ctx.strokeStyle = P.accent; ctx.lineWidth = 1.6;
            h.rrect(ctx, c[1].x, c[1].y - 17, c[1].w, 34, 9); ctx.fill(); ctx.stroke();
            h.label(ctx, c[0], c[1].x + c[1].w / 2, c[1].y, P.accent, 12.5, 'center', '700');
          });
        }
        var score = Math.min(100, Math.round(20 + insul * 8 + solar * 4 + green * 5));
        // 楼体
        var bx = 120, by = 90, bw = 220, bh = 200;
        ctx.fillStyle = 'rgba(148,163,184,.35)'; h.rrect(ctx, bx, by, bw, bh, 8); ctx.fill();
        ctx.strokeStyle = P.grid; ctx.lineWidth = 2; h.rrect(ctx, bx, by, bw, bh, 8); ctx.stroke();
        // 保温层
        ctx.strokeStyle = P.accent2; ctx.lineWidth = 3 + insul * 1.6; ctx.globalAlpha = 0.65;
        h.rrect(ctx, bx - 6, by - 6, bw + 12, bh + 12, 10); ctx.stroke(); ctx.globalAlpha = 1;
        // 窗户（太阳能板越多，屋顶板越多）
        for (var i = 0; i < 3; i++) {
          for (var j = 0; j < 3; j++) {
            ctx.fillStyle = (i + j) % 3 === 0 && solar > 2 ? '#fbbf24' : 'rgba(96,165,250,.6)';
            h.rrect(ctx, bx + 24 + i * 66, by + 26 + j * 56, 46, 34, 4); ctx.fill();
          }
        }
        // 太阳能板
        for (var k = 0; k < solar; k++) {
          ctx.fillStyle = '#0ea5e9';
          h.rrect(ctx, bx + 8 + k * 34, by - 34, 30, 22, 4); ctx.fill();
        }
        // 绿化
        for (var g = 0; g < green; g++) {
          ctx.beginPath(); ctx.arc(bx + bw + 40 + g * 34, by + bh - 14, 16, 0, Math.PI * 2); ctx.fillStyle = 'rgba(34,197,94,.7)'; ctx.fill();
          ctx.fillStyle = '#a16207'; ctx.fillRect(bx + bw + 38 + g * 34, by + bh - 6, 4, 12);
        }
        h.label(ctx, '🏢 你设计的绿色建筑', bx + bw / 2, by + bh + 30, P.ink, 13, 'center', '700');
        // 评分环
        var cx2 = W - 130, cy2 = H / 2, R = 58;
        ctx.beginPath(); ctx.arc(cx2, cy2, R, 0, Math.PI * 2); ctx.strokeStyle = 'rgba(148,163,184,.3)'; ctx.lineWidth = 12; ctx.stroke();
        ctx.beginPath(); ctx.arc(cx2, cy2, R, -Math.PI / 2, -Math.PI / 2 + 2 * Math.PI * score / 100);
        ctx.strokeStyle = score >= 70 ? P.ok : score >= 45 ? P.accent2 : P.bad; ctx.lineWidth = 12; ctx.stroke();
        h.label(ctx, score + '', cx2, cy2 - 6, P.ink, 26, 'center', '800');
        h.label(ctx, '节能评分', cx2, cy2 + 22, P.muted, 12, 'center', '600');
        this.readout('保温 ' + insul + ' 级、太阳能板 ' + solar + ' 块、绿化 ' + green + ' 处 → 节能评分 ' + score +
          ' 分。' + (score >= 70 ? '很棒！保温+可再生+绿化三管齐下，建筑能耗显著下降。'
                                : '试试同时提高三项：单靠一项效果有限，绿色建筑是“组合拳”。'));
      }
    });
  }

  /* ---------- 15) 天气日历：点击日期设置天气 → 统计 ---------- */
  function calendar(cfg) {
    var kinds = cfg.kinds || [{ n: '晴', e: '☀️' }, { n: '多云', e: '⛅' }, { n: '阴', e: '☁️' }, { n: '雨', e: '🌧️' }];
    var days = 14;
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'pointer',
      initial: { data: {}, sel: null }, sharedState: cfg.sharedState,
      onPointer: function (type, p, s) {
        if (type !== 'pointerdown') return;
        var f = this.fit(), cols = 7, cw = (f.W - 60) / cols, ch = (f.H - 110) / 2;
        for (var i = 0; i < days; i++) {
          var x = 30 + (i % cols) * cw, y = 70 + Math.floor(i / cols) * ch;
          if (p.x > x && p.x < x + cw - 8 && p.y > y && p.y < y + ch - 8) {
            var cur = s.data[i];
            var idx = kinds.findIndex(function (k) { return k.n === cur; });
            var nxt = (idx + 1) % (kinds.length + 1);
            if (nxt === kinds.length) { delete s.data[i]; } else { s.data[i] = kinds[nxt].n; }
            return;
          }
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var cols = 7, cw = (W - 60) / cols, ch = (H - 110) / 2;
        h.label(ctx, '📅 天气日历（点击格子切换天气，再统计）', W / 2, 30, P.ink, 14, 'center', '800');
        for (var i = 0; i < days; i++) {
          var x = 30 + (i % cols) * cw, y = 70 + Math.floor(i / cols) * ch;
          var cur = s.data[i] || '';
          var kind = kinds.find(function (k) { return k.n === cur; });
          ctx.fillStyle = cur ? 'rgba(96,165,250,.16)' : 'rgba(148,163,184,.12)';
          ctx.strokeStyle = cur ? P.accent : P.grid; ctx.lineWidth = 1.6;
          h.rrect(ctx, x, y, cw - 8, ch - 8, 10); ctx.fill(); ctx.stroke();
          h.label(ctx, String(i + 1), x + 14, y + 14, P.muted, 11.5, 'left', '600');
          h.label(ctx, kind ? kind.e + ' ' + kind.n : '—', x + (cw - 8) / 2, y + (ch - 8) / 2 + 4, P.ink, 15, 'center', '700');
        }
        var cnt = {};
        Object.keys(s.data).forEach(function (k) { cnt[s.data[k]] = (cnt[s.data[k]] || 0) + 1; });
        var total = Object.keys(s.data).length;
        var txt = kinds.map(function (k) { return k.n + ' ' + (cnt[k.n] || 0) + ' 天'; }).join('｜');
        h.label(ctx, '统计：' + (total ? txt : '还没记录，点格子开始'), W / 2, H - 18, P.accent, 12.5, 'center', '700');
        this.readout(total
          ? '已记录 ' + total + ' 天：' + txt + '。天气是短时间的大气状况——同一天气反复出现，才能说“这段时间以某天气为主”。'
          : '点击日历格子记录每天的天气，再看哪种天气出现得最多。');
      }
    });
  }

  /* ---------- 16) 分类树：可点击节点 ---------- */
  function tree(cfg) {
    var nodes = cfg.nodes || [];
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'pointer', sharedState: cfg.sharedState,
      initial: { sel: null, hover: null },
      onPointer: function (type, p, s) {
        var best = null, bd = 1e9;
        nodes.forEach(function (nd, i) {
          var d = Math.hypot(p.x - nd.x, p.y - nd.y);
          if (d < (nd.r || 40) && d < bd) { bd = d; best = i; }
        });
        if (type === 'pointermove') { s.hover = best; }
        if (type === 'pointerdown') { s.sel = best; }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        // 连线
        (cfg.edges || []).forEach(function (e) {
          var a = nodes[e[0]], b = nodes[e[1]];
          if (!a || !b) return;
          ctx.strokeStyle = P.grid; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.moveTo(a.x, a.y + 18); ctx.lineTo(b.x, b.y - 18); ctx.stroke();
        });
        nodes.forEach(function (nd, i) {
          var on = (s.sel === i) || (s.hover === i);
          ctx.fillStyle = nd.color || (on ? P.fill : 'rgba(148,163,184,.18)');
          ctx.strokeStyle = on ? P.accent : P.grid; ctx.lineWidth = on ? 2.6 : 1.6;
          h.rrect(ctx, nd.x - (nd.w || 62), nd.y - 18, (nd.w || 62) * 2, 36, 10); ctx.fill(); ctx.stroke();
          h.label(ctx, nd.name, nd.x, nd.y, on ? P.accent : P.ink, 13, 'center', '700');
        });
        var cur = s.sel != null ? nodes[s.sel] : null;
        this.readout(cur ? (cur.name + '：' + (cur.info || '')) : (cfg.hint || '👆 点击分类树的节点，看这一类的共同特征。'));
      }
    });
  }


  /* ---------- 17) 圆的几何：弦/切线/圆周角/弧长（mode 驱动，sliders 真实计算） ---------- */
  function circleGeo(cfg) {
    var mode = cfg.mode;
    var sliders = {};
    if (mode === 'chord') sliders.len = { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '弦长 ' + v; } };
    if (mode === 'tangent') sliders.d = { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '点到圆心距离 ' + v; } };
    if (mode === 'angle') sliders.ang = { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '圆心角 ' + v + '°'; } };
    if (mode === 'arc') {
      sliders.r = { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '半径 ' + v; } };
      sliders.a = { el: cfg.slider2, out: cfg.slider2Out, fmt: function (v) { return '圆心角 ' + v + '°'; } };
    }
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, sliders: sliders, sharedState: cfg.sharedState,
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var cx = W / 2, cy = H / 2 + 6, R = Math.min(W, H) * 0.33;
        // 圆
        ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.strokeStyle = P.grid; ctx.lineWidth = 2; ctx.stroke();
        ctx.beginPath(); ctx.arc(cx, cy, 3, 0, Math.PI * 2); ctx.fillStyle = P.muted; ctx.fill();
        h.label(ctx, 'O', cx - 12, cy + 12, P.muted, 12, 'center', '700');
        if (mode === 'chord') {
          var L = Math.max(10, Math.min(2 * R * 0.98, (s.len || 20) * (R / 14)));
          var half = L / 2, d = Math.sqrt(Math.max(0, R * R - half * half));
          ctx.strokeStyle = P.accent; ctx.lineWidth = 3;
          ctx.beginPath(); ctx.moveTo(cx - half, cy - d); ctx.lineTo(cx + half, cy - d); ctx.stroke();
          ctx.setLineDash([4, 4]); ctx.strokeStyle = P.accent2; ctx.lineWidth = 1.6;
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx, cy - d); ctx.stroke(); ctx.setLineDash([]);
          h.label(ctx, '弦 AB=' + (L / (R / 14)).toFixed(1), cx, cy - d - 16, P.accent, 12.5, 'center', '700');
          h.label(ctx, '弦心距 d=' + (d / (R / 14)).toFixed(1), cx + 8, cy - d / 2, P.accent2, 12, 'left', '700');
          this.readout('在同圆中，弦越长，弦心距越小；过圆心垂直于弦的直径平分这条弦（垂径定理）。弦长 ' +
            (L / (R / 14)).toFixed(1) + ' → 弦心距 ' + (d / (R / 14)).toFixed(1) + '。');
        } else if (mode === 'tangent') {
          var pv = s.d || 20, pp = R * (pv / 20);
          var px = cx + pp, py = cy;
          ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI * 2); ctx.fillStyle = P.accent2; ctx.fill();
          h.label(ctx, 'P', px + 12, py - 12, P.accent2, 12.5, 'center', '700');
          if (pp >= R - 2) {
            var tlen = Math.sqrt(Math.max(0, pp * pp - R * R));
            var ang = Math.acos(R / pp);
            var tx = cx + R * Math.cos(ang), ty = cy + R * Math.sin(ang);
            ctx.strokeStyle = P.accent; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(tx, ty); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(tx, ty); ctx.strokeStyle = P.ok; ctx.lineWidth = 2; ctx.stroke();
            h.label(ctx, '切线长 ' + (tlen / (R / 20)).toFixed(1), (px + tx) / 2 + 10, (py + ty) / 2 - 12, P.accent, 12, 'center', '700');
            this.readout('从圆外一点引切线：切线长 = √(OP² − r²)。OP=' + (pp / (R / 20)).toFixed(1) +
              '，r=20 → 切线长 ' + (tlen / (R / 20)).toFixed(1) + '。切线还垂直于过切点的半径。');
          } else {
            this.readout('点在圆内（OP=' + (pp / (R / 20)).toFixed(1) + ' < r=20）：过圆内一点不能作圆的切线。把点拖到圆外试试。');
          }
        } else if (mode === 'angle') {
          var a = (s.ang || 90) * Math.PI / 180;
          // 圆心角
          ctx.strokeStyle = P.accent; ctx.lineWidth = 3;
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + R * Math.cos(-0.6), cy + R * Math.sin(-0.6)); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + R * Math.cos(-0.6 + a), cy + R * Math.sin(-0.6 + a)); ctx.stroke();
          // 圆周角（同弧）
          var px2 = cx + R * Math.cos(1.9), py2 = cy + R * Math.sin(1.9);
          ctx.strokeStyle = P.accent2; ctx.lineWidth = 2.4;
          ctx.beginPath(); ctx.moveTo(px2, py2); ctx.lineTo(cx + R * Math.cos(-0.6), cy + R * Math.sin(-0.6)); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(px2, py2); ctx.lineTo(cx + R * Math.cos(-0.6 + a), cy + R * Math.sin(-0.6 + a)); ctx.stroke();
          h.label(ctx, '圆心角 ' + (s.ang || 90) + '°', cx + 10, cy - 18, P.accent, 12.5, 'left', '700');
          h.label(ctx, '圆周角 ' + ((s.ang || 90) / 2).toFixed(1) + '°', px2 - 20, py2 - 16, P.accent2, 12.5, 'center', '700');
          this.readout('同弧所对的圆周角等于圆心角的一半：圆心角 ' + (s.ang || 90) + '° → 圆周角 ' +
            ((s.ang || 90) / 2).toFixed(1) + '°。');
        } else {
          var rr = Math.min(R, (s.r || 8) * (R / 12));
          var aa = (s.a || 90) * Math.PI / 180;
          ctx.fillStyle = 'rgba(2,132,199,.18)';
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, rr, 0, aa); ctx.closePath(); ctx.fill();
          ctx.strokeStyle = P.accent; ctx.lineWidth = 2.6;
          ctx.beginPath(); ctx.arc(cx, cy, rr, 0, aa); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + rr, cy); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + rr * Math.cos(aa), cy + rr * Math.sin(aa)); ctx.stroke();
          var len = rr * aa, area = 0.5 * rr * rr * aa;
          h.label(ctx, '弧长 = ' + (s.a || 90) + '/360 × 2πr ≈ ' + (len / (R / 12)).toFixed(1), W / 2, 26, P.accent, 12.5, 'center', '700');
          h.label(ctx, '扇形面积 ≈ ' + (area / (R / 12) / (R / 12)).toFixed(1), W / 2, H - 22, P.muted, 12, 'center', '600');
          this.readout('弧长 = 圆心角/360 × 2πr，扇形面积 = 圆心角/360 × πr²。r=' + (rr / (R / 12)).toFixed(1) +
            '、圆心角 ' + (s.a || 90) + '° → 弧长约 ' + (len / (R / 12)).toFixed(1) + '。');
        }
      }
    });
  }

  /* ---------- 18) 正比例 / 反比例 函数图像（k 可调） ---------- */
  function proportion(cfg) {
    var inv = cfg.mode === 'inverse';
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, sharedState: cfg.sharedState,
      sliders: { k: { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return 'k = ' + v; } } },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var ox = W / 2, oy = H / 2, u = Math.min(W, H) / 12;
        // 坐标轴
        ctx.strokeStyle = P.grid; ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.moveTo(20, oy); ctx.lineTo(W - 20, oy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(ox, 20); ctx.lineTo(ox, H - 20); ctx.stroke();
        h.label(ctx, 'x', W - 26, oy - 12, P.muted, 12, 'center', '600');
        h.label(ctx, 'y', ox + 14, 26, P.muted, 12, 'center', '600');
        for (var i = -5; i <= 5; i++) {
          if (i === 0) continue;
          ctx.beginPath(); ctx.moveTo(ox + i * u, oy - 4); ctx.lineTo(ox + i * u, oy + 4); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(ox - 4, oy + i * u); ctx.lineTo(ox + 4, oy + i * u); ctx.stroke();
        }
        var k = (typeof s.k === 'number' && !isNaN(s.k)) ? s.k : 1;
        ctx.strokeStyle = P.accent; ctx.lineWidth = 3; ctx.beginPath();
        if (!inv) {
          var first = true;
          for (var px = -5; px <= 5; px += 0.05) {
            var X = ox + px * u, Y = oy - k * px * u;
            if (Y < 16 || Y > H - 16) { first = true; continue; }
            first ? ctx.moveTo(X, Y) : ctx.lineTo(X, Y); first = false;
          }
          ctx.stroke();
          h.label(ctx, 'y = ' + k + 'x（直线，过原点）', W / 2, 26, P.accent, 13, 'center', '700');
          this.readout('正比例函数 y = kx：图像是过原点的一条直线。k = ' + k +
            (k > 0 ? '，y 随 x 增大而增大（第一、三象限）。' : k < 0 ? '，y 随 x 增大而减小（第二、四象限）。' : '，此时 y 恒为 0。'));
        } else {
          var fp = true, fn = true;
          for (var qx2 = 0.06; qx2 <= 6; qx2 += 0.02) {
            var X2 = ox + qx2 * u, Y2 = oy - (k / qx2) * u;
            if (Y2 > 14 && Y2 < H - 14) { fp ? ctx.moveTo(X2, Y2) : ctx.lineTo(X2, Y2); fp = false; }
            var X3 = ox - qx2 * u, Y3 = oy + (k / qx2) * u;
            if (Y3 > 14 && Y3 < H - 14) { fn ? ctx.moveTo(X3, Y3) : ctx.lineTo(X3, Y3); fn = false; }
          }
          ctx.stroke();
          h.label(ctx, 'y = ' + k + '/x（双曲线，两支）', W / 2, 26, P.accent, 13, 'center', '700');
          this.readout('反比例函数 y = k/x：图像是双曲线，两支分别在第一、三象限（k>0）或第二、四象限（k<0）。k = ' +
            k + '；x 越大，y 越小（但不是直线下降）。');
        }
      }
    });
  }

  /* ---------- 19) 相交线/平行线截线：角度关系 ---------- */
  function lineAngle(cfg) {
    var par = cfg.mode === 'transversal';
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'grab', sharedState: cfg.sharedState,
      initial: { ang: 60, dragging: false },
      onPointer: function (type, p, s) {
        var f = this.fit();
        if (type === 'pointerdown') s.dragging = true;
        if (type === 'pointerup' || type === 'pointerleave') s.dragging = false;
        if (s.dragging && type === 'pointermove') {
          var a = Math.atan2(f.H / 2 - p.y, W2(f) - p.x) * 180 / Math.PI;
          s.ang = Math.max(15, Math.min(165, Math.abs(a)));
        }
        function W2(ff) { return ff.W / 2; }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var a = (s.ang || 60) * Math.PI / 180;
        if (!par) {
          var ox = W / 2, oy = H / 2, L = Math.min(W, H) * 0.42;
          ctx.strokeStyle = P.accent; ctx.lineWidth = 2.6;
          ctx.beginPath(); ctx.moveTo(ox - L, oy); ctx.lineTo(ox + L, oy); ctx.stroke();
          ctx.strokeStyle = P.accent2;
          ctx.beginPath(); ctx.moveTo(ox - L * Math.cos(a), oy + L * Math.sin(a)); ctx.lineTo(ox + L * Math.cos(a), oy - L * Math.sin(a)); ctx.stroke();
          h.label(ctx, '∠1 = ' + Math.round(s.ang) + '°', ox + 46, oy - 16, P.ink, 12.5, 'left', '700');
          h.label(ctx, '∠2 = ' + Math.round(180 - s.ang) + '°（邻补角，和为 180°）', ox - 46, oy - 16, P.accent, 12.5, 'right', '700');
          h.label(ctx, '∠3 = ' + Math.round(180 - s.ang) + '°（对顶角，与 ∠2 相等）', ox + 46, oy + 24, P.muted, 12, 'left', '600');
          this.readout('两条直线相交：对顶角相等，邻补角互补（和为 180°）。现在 ∠1=' + Math.round(s.ang) +
            '°，则它的对顶角也是 ' + Math.round(s.ang) + '°，邻补角是 ' + Math.round(180 - s.ang) + '°。');
        } else {
          var y1 = H * 0.32, y2 = H * 0.68, m = 60;
          ctx.strokeStyle = P.accent; ctx.lineWidth = 2.6;
          ctx.beginPath(); ctx.moveTo(m, y1); ctx.lineTo(W - m, y1); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(m, y2); ctx.lineTo(W - m, y2); ctx.stroke();
          ctx.strokeStyle = P.accent2; ctx.lineWidth = 2.6;
          var dx = 90 * Math.cos(a), dy = 90 * Math.sin(a);
          ctx.beginPath(); ctx.moveTo(W / 2 - dx * 2, y1 + dy * -2); ctx.lineTo(W / 2 + dx * 2, y2 + dy * 0.6); ctx.stroke();
          h.label(ctx, '两条平行线被第三条直线所截', W / 2, 22, P.ink, 13, 'center', '700');
          h.label(ctx, '同位角相等 · 内错角相等 · 同旁内角互补', W / 2, H - 20, P.accent, 13, 'center', '700');
          this.readout('平行线的性质：两直线平行 → 同位角相等、内错角相等、同旁内角互补；反过来，这些关系成立也能判定两直线平行。');
        }
      }
    });
  }

  /* ---------- 20) 旋转 / 尺规作图 / 轴对称（mode 驱动） ---------- */
  function rotation(cfg) {
    var mode = cfg.mode;
    var sliders = {};
    if (mode === 'rotate') sliders.ang = { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '旋转角 ' + v + '°'; } };
    if (mode === 'construct') sliders.ang = { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return '目标角 ' + v + '°'; } };
    if (mode === 'symmetry') sliders.n = { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return v + ' 条对称轴'; } };
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, sliders: sliders, sharedState: cfg.sharedState,
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var cx = W / 2, cy = H / 2 + 10, size = Math.min(W, H) * 0.26;
        // 原图形（三角形）
        var pts = [[-size, size * 0.6], [size * 0.9, size * 0.6], [0, -size * 0.7]];
        function poly(pts2, color, fill) {
          ctx.beginPath();
          pts2.forEach(function (pt, i) { i ? ctx.lineTo(cx + pt[0], cy + pt[1]) : ctx.moveTo(cx + pt[0], cy + pt[1]); });
          ctx.closePath();
          if (fill) { ctx.fillStyle = fill; ctx.fill(); }
          ctx.strokeStyle = color; ctx.lineWidth = 2.6; ctx.stroke();
        }
        if (mode === 'rotate') {
          var a = (s.ang || 90) * Math.PI / 180;
          poly(pts, P.grid, 'rgba(148,163,184,.2)');
          poly(pts.map(function (pt) { return [pt[0] * Math.cos(a) - pt[1] * Math.sin(a), pt[0] * Math.sin(a) + pt[1] * Math.cos(a)]; }), P.accent, 'rgba(2,132,199,.16)');
          h.label(ctx, '绕点 O 旋转 ' + (s.ang || 90) + '°', W / 2, 24, P.accent, 13, 'center', '700');
          this.readout('旋转不改变图形的形状和大小（全等），只改变位置和方向：对应点到旋转中心的距离相等，对应点与旋转中心连线的夹角等于旋转角 ' + (s.ang || 90) + '°。');
        } else if (mode === 'construct') {
          poly(pts, P.accent, 'rgba(2,132,199,.16)');
          var a2 = (s.ang || 60) * Math.PI / 180;
          ctx.strokeStyle = P.accent2; ctx.lineWidth = 1.8; ctx.setLineDash([5, 4]);
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + size * 1.3, cy); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + size * 1.3 * Math.cos(a2), cy - size * 1.3 * Math.sin(a2)); ctx.stroke();
          ctx.setLineDash([]);
          ctx.beginPath(); ctx.arc(cx, cy, size * 1.1, -a2, 0); ctx.strokeStyle = P.ok; ctx.lineWidth = 2; ctx.stroke();
          h.label(ctx, '尺规作一个角等于 ' + (s.ang || 60) + '°：以 O 为圆心画弧 → 量取弧长 → 在新位置截取同样弧长 → 连线', W / 2, H - 18, P.ok, 12, 'center', '700');
          this.readout('尺规作图作等角：① 以顶点 O 为圆心、任意半径画弧，交两边于 A、B；② 画射线 O′A′，以 O′ 为圆心、同半径画弧；③ 用圆规量取 AB 长度，在弧上截取 A′B′；④ 连 O′B′，所得角等于原角 ' + (s.ang || 60) + '°。');
        } else {
          var n = s.n || 3;
          poly(pts, P.accent, 'rgba(2,132,199,.16)');
          for (var i = 0; i < n; i++) {
            var ang2 = i * Math.PI / n;
            ctx.strokeStyle = 'rgba(251,191,36,.85)'; ctx.lineWidth = 1.6; ctx.setLineDash([5, 4]);
            ctx.beginPath();
            ctx.moveTo(cx - size * 1.5 * Math.cos(ang2), cy - size * 1.5 * Math.sin(ang2));
            ctx.lineTo(cx + size * 1.5 * Math.cos(ang2), cy + size * 1.5 * Math.sin(ang2));
            ctx.stroke();
          }
          ctx.setLineDash([]);
          h.label(ctx, '对称轴 ' + n + ' 条', W / 2, 24, P.accent2, 13, 'center', '700');
          this.readout(n + ' 条对称轴把图形分成 ' + (2 * n) + ' 个全等的部分；轴对称图形沿对称轴折叠后两边完全重合。一般三角形没有对称轴，等腰三角形有 1 条，等边三角形有 3 条。');
        }
      }
    });
  }

  /* ---------- 21) 三角形：拖动顶点看内角和恒为 180° ---------- */
  function triangle(cfg) {
    var fixed = cfg.mode === 'anglesum';
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'grab', sharedState: cfg.sharedState,
      initial: { ax: -110, ay: 70, bx: 120, by: 70, cx: -10, cy: -90, drag: null },
      onPointer: function (type, p, s) {
        var f = this.fit(), cx = f.W / 2, cy = f.H / 2 + 10;
        var pts = ['a', 'b', 'c'];
        if (type === 'pointerdown') {
          var best = null, bd = 1e9;
          pts.forEach(function (k) {
            var d = Math.hypot(p.x - (cx + s[k + 'x']), p.y - (cy + s[k + 'y']));
            if (d < 26 && d < bd) { bd = d; best = k; }
          });
          s.drag = best;
        }
        if (type === 'pointerup' || type === 'pointerleave') s.drag = null;
        if (s.drag && type === 'pointermove') {
          s[s.drag + 'x'] = Math.max(-f.W / 2 + 30, Math.min(f.W / 2 - 30, p.x - cx));
          s[s.drag + 'y'] = Math.max(-f.H / 2 + 40, Math.min(f.H / 2 - 30, p.y - cy));
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var cx = W / 2, cy = H / 2 + 10;
        var A = [cx + s.ax, cy + s.ay], B = [cx + s.bx, cy + s.by], C = [cx + s.cx, cy + s.cy];
        function ang(P1, P2, P3) {
          var v1 = [P1[0] - P2[0], P1[1] - P2[1]], v2 = [P3[0] - P2[0], P3[1] - P2[1]];
          var d = (v1[0] * v2[0] + v1[1] * v2[1]) / (Math.hypot.apply(null, v1) * Math.hypot.apply(null, v2));
          return Math.acos(Math.max(-1, Math.min(1, d))) * 180 / Math.PI;
        }
        var Aa = ang(B, A, C), Ba = ang(A, B, C), Ca = ang(A, C, B);
        ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.lineTo(C[0], C[1]); ctx.closePath();
        ctx.fillStyle = 'rgba(2,132,199,.14)'; ctx.fill();
        ctx.strokeStyle = P.accent; ctx.lineWidth = 2.6; ctx.stroke();
        [[A, 'A'], [B, 'B'], [C, 'C']].forEach(function (pt) {
          ctx.beginPath(); ctx.arc(pt[0][0], pt[0][1], 6, 0, Math.PI * 2); ctx.fillStyle = P.accent2; ctx.fill();
          h.label(ctx, pt[1], pt[0][0] + 16, pt[0][1] - 14, P.ink, 13, 'center', '800');
        });
        h.label(ctx, '∠A=' + Aa.toFixed(1) + '°　∠B=' + Ba.toFixed(1) + '°　∠C=' + Ca.toFixed(1) + '°',
          W / 2, 24, P.accent, 13, 'center', '700');
        h.label(ctx, '内角和 = ' + (Aa + Ba + Ca).toFixed(1) + '°（恒为 180°）', W / 2, H - 20, P.ok, 13.5, 'center', '800');
        this.readout('任意三角形三个内角的和都是 180°。现在 ∠A+∠B+∠C = ' + (Aa + Ba + Ca).toFixed(1) +
          '°；拖动顶点改变形状，和仍然是 180°。（三角形的外角等于与它不相邻的两个内角之和）');
      }
    });
  }


  /* ---------- 22) 历史时间轴：拖动光标 / 切换文明 ---------- */
  function timeline(cfg) {
    var civs = cfg.civs || [];
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'ew-resize', sharedState: cfg.sharedState,
      initial: { year: cfg.startYear || -3500, filter: 'all', dragging: false },
      onPointer: function (type, p, s) {
        var f = this.fit();
        if (type === 'pointerdown') s.dragging = true;
        if (type === 'pointerup' || type === 'pointerleave') s.dragging = false;
        if (s.dragging && type === 'pointermove') {
          var t = Math.max(0, Math.min(1, (p.x - 70) / (f.W - 120)));
          var span = (cfg.endYear || 500) - (cfg.startYear || -3500);
          s.year = Math.round((cfg.startYear || -3500) + t * span);
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var y0 = cfg.startYear || -3500, y1 = cfg.endYear || 500;
        var x0 = 70, x1 = W - 50, yy = 96;
        function X(y) { return x0 + (y - y0) / (y1 - y0) * (x1 - x0); }
        // 主轴
        ctx.strokeStyle = P.grid; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(x0, yy); ctx.lineTo(x1, yy); ctx.stroke();
        for (var y = Math.ceil(y0 / 500) * 500; y <= y1; y += 500) {
          var xx = X(y);
          ctx.beginPath(); ctx.moveTo(xx, yy - 5); ctx.lineTo(xx, yy + 5); ctx.stroke();
          if (y % 1000 === 0) h.label(ctx, y < 0 ? '前' + (-y) : String(y), xx, yy + 22, P.muted, 11, 'center', '600');
        }
        // 各文明兴衰条
        var rows = civs.filter(function (c) { return s.filter === 'all' || c.key === s.filter; });
        rows.forEach(function (c, i) {
          var ry = 30 + i * 40;
          ctx.strokeStyle = c.color; ctx.lineWidth = 12; ctx.globalAlpha = 0.45;
          ctx.beginPath(); ctx.moveTo(X(c.from), ry); ctx.lineTo(X(c.to), ry); ctx.stroke();
          ctx.globalAlpha = 1;
          h.label(ctx, c.name, x0 - 12, ry, P.ink, 12.5, 'right', '700');
          (c.events || []).forEach(function (ev) {
            var ex = X(ev[0]);
            ctx.beginPath(); ctx.arc(ex, ry, 5, 0, Math.PI * 2); ctx.fillStyle = c.color; ctx.fill();
            if (Math.abs(ev[0] - s.year) < 320) h.label(ctx, ev[1], ex, ry - 16, P.accent, 11.5, 'center', '700');
          });
        });
        // 光标
        var cx = X(s.year);
        ctx.strokeStyle = P.accent2; ctx.lineWidth = 2; ctx.setLineDash([4, 4]);
        ctx.beginPath(); ctx.moveTo(cx, 16); ctx.lineTo(cx, H - 40); ctx.stroke(); ctx.setLineDash([]);
        h.label(ctx, (s.year < 0 ? '公元前 ' + (-s.year) + ' 年' : '公元 ' + s.year + ' 年'), cx, H - 22, P.accent2, 13, 'center', '800');
        var near = [];
        civs.forEach(function (c) {
          (c.events || []).forEach(function (ev) {
            if (Math.abs(ev[0] - s.year) < 200) near.push(c.name + '：' + ev[1] + '（' + (ev[0] < 0 ? '前' + (-ev[0]) : ev[0]) + '）');
          });
        });
        this.readout(near.length ? '此时发生：' + near.slice(0, 3).join('；')
          : '拖动时间轴光标，观察各文明的兴衰节奏与同期事件（大河文明都依托河流、都在约公元前 3500—前 500 年之间兴起）。');
      }
    });
  }

  /* ---------- 23) 印刷术扩散：印刷机数量 → 传播天数 ---------- */
  function diffusion(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, sharedState: cfg.sharedState,
      sliders: {
        presses: { el: cfg.slider, out: cfg.sliderOut, fmt: function (v) { return v + ' 台'; } },
        daily: { el: cfg.slider2, out: cfg.slider2Out, fmt: function (v) { return v + ' 份/台·天'; } }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var press = s.presses || 1, daily = s.daily || 10;
        var perDay = press * daily;
        var days = Math.max(1, Math.ceil(3000 / perDay));       // 假设需要覆盖 3000 份
        // 城墙示意 + 传单扩散
        var cx = 150, cy = H / 2 + 10;
        ctx.fillStyle = 'rgba(148,163,184,.45)'; h.rrect(ctx, cx - 70, cy - 40, 140, 80, 10); ctx.fill();
        h.label(ctx, '维滕堡', cx, cy, P.ink, 13, 'center', '800');
        ctx.beginPath(); ctx.arc(cx - 96, cy + 34, 12, 0, Math.PI * 2); ctx.fillStyle = P.accent2; ctx.fill();
        h.label(ctx, '🖨', cx - 96, cy + 34, '#fff', 12, 'center', '800');
        // 扩散进度条
        var bw = W - 380, bx = 300, by = cy - 26;
        ctx.fillStyle = 'rgba(148,163,184,.25)'; h.rrect(ctx, bx, by, bw, 26, 8); ctx.fill();
        var pct = Math.min(1, (1 / days) * 4);
        ctx.fillStyle = P.accent; h.rrect(ctx, bx, by, Math.max(6, bw * Math.min(1, pct + 0.15)), 26, 8); ctx.fill();
        h.label(ctx, '每台每天 ' + daily + ' 份 · 共 ' + press + ' 台 → 每天 ' + perDay + ' 份', bx, by - 18, P.muted, 12.5, 'left', '600');
        h.label(ctx, '覆盖 3000 份约需 ' + days + ' 天', bx + bw / 2, by + 60, P.accent, 16, 'center', '800');
        // 对比：手抄
        h.label(ctx, '（手抄：一个抄书匠抄一本约需数月）', bx + bw / 2, by + 92, P.bad, 12.5, 'center', '700');
        this.readout('印刷机 ' + press + ' 台、每台每天 ' + daily + ' 份 → 每天 ' + perDay +
          ' 份，覆盖 3000 份只需约 ' + days + ' 天。这就是印刷术的“放大器”效应：路德的《九十五条论纲》因此几周内传遍德意志。');
      }
    });
  }

  /* ---------- 24) 凸透镜成像（物距/焦距 → 像的性质） ---------- */
  function lens(cfg) {
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, sharedState: cfg.sharedState,
      sliders: {
        u: { el: cfg.sliderA, fmt: function (v) { return v; } },
        f: { el: cfg.sliderB, fmt: function (v) { return v; } }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var u = (typeof s.u === 'number' ? s.u : 6) * 1.0;     // 物距（格）
        var f = (typeof s.f === 'number' ? s.f : 3) * 1.0;     // 焦距（格）
        var cy = H / 2, scale = Math.min(W / 22, H / 8);
        var ox = W / 2, uu = Math.max(0.6, u), ff = Math.max(0.5, f);
        var inv = 1 / uu - 1 / ff;
        var v = inv === 0 ? Infinity : 1 / inv;
        // 主光轴 + 透镜
        ctx.strokeStyle = P.grid; ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.moveTo(20, cy); ctx.lineTo(W - 20, cy); ctx.stroke();
        ctx.strokeStyle = P.accent; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.ellipse(ox, cy, 12, scale * 2.6, 0, 0, Math.PI * 2); ctx.stroke();
        h.label(ctx, '凸透镜', ox, cy - scale * 2.6 - 14, P.accent, 12, 'center', '700');
        // 焦点
        [-1, 1].forEach(function (sg) {
          ctx.beginPath(); ctx.arc(ox + sg * ff * scale, cy, 4, 0, Math.PI * 2); ctx.fillStyle = P.accent2; ctx.fill();
          h.label(ctx, 'F', ox + sg * ff * scale, cy + 16, P.accent2, 11.5, 'center', '700');
        });
        // 物（箭头，向上为正）
        var oh = scale * 1.6;
        var objX = ox - uu * scale;
        h.arrow(ctx, objX, cy, objX, cy - oh, P.ok, 3);
        h.label(ctx, '物', objX - 14, cy - oh / 2, P.ok, 12.5, 'center', '700');
        // 三条特殊光线
        var apex = [objX, cy - oh];
        ctx.strokeStyle = 'rgba(239,68,68,.75)'; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(apex[0], apex[1]); ctx.lineTo(ox, apex[1]); ctx.lineTo(W - 30, cy + (cy - apex[1]) * 1.0); ctx.stroke();
        ctx.strokeStyle = 'rgba(96,165,250,.75)';
        ctx.beginPath(); ctx.moveTo(apex[0], apex[1]); ctx.lineTo(ox, cy); ctx.lineTo(W - 30, cy + (cy - apex[1])); ctx.stroke();
        // 像
        var nature;
        if (isFinite(v) && v > 0) {
          var ih = -oh * (v / uu);            // 实像倒立
          var imgX = ox + v * scale;
          if (imgX < W - 24) {
            h.arrow(ctx, imgX, cy, imgX, cy + Math.abs(ih), P.bad, 3);
            h.label(ctx, '像', imgX + 14, cy + Math.abs(ih) / 2, P.bad, 12.5, 'center', '700');
          }
          nature = (v > uu ? '倒立、放大的实像（v=' + v.toFixed(1) + ' 格 > u，投影仪原理）'
                           : v < uu ? '倒立、缩小的实像（v=' + v.toFixed(1) + ' 格 < u，照相机原理）'
                                    : '倒立、等大的实像（u = v = 2f）');
        } else if (Math.abs(uu - ff) < 0.15) {
          nature = '不成像（物体正好在焦点上，折射光线平行射出）';
        } else {
          nature = '正立、放大的虚像（物体在焦点以内，同侧，放大镜原理）';
        }
        h.label(ctx, 'u = ' + uu.toFixed(1) + ' 格　f = ' + ff.toFixed(1) + ' 格', W - 24, 24, P.accent, 12.5, 'right', '700');
        h.label(ctx, nature, W / 2, H - 22, P.ink, 13, 'center', '700');
        var el = document.getElementById(cfg.readout);
        if (el) el.textContent = '物距 u=' + uu.toFixed(1) + '，焦距 f=' + ff.toFixed(1) + ' → ' + nature +
          '。规律：u>2f 缩小实像；f<u<2f 放大实像；u<f 正立放大虚像；u=2f 等大实像。';
      }
    });
  }

  /* ---------- 25) 复分解反应：离子结合生成沉淀 ---------- */
  function reaction(cfg) {
    var pairs = cfg.pairs || [];
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'pointer', sharedState: cfg.sharedState,
      initial: { sel: 0, t: 0, playing: true, formed: 0 },
      onPointer: function (type, p, s) {
        if (type !== 'pointerdown') return;
        var f = this.fit(), n = pairs.length, w = (f.W - 40) / Math.max(1, n);
        for (var i = 0; i < n; i++) {
          if (p.x > 20 + i * w && p.x < 20 + (i + 1) * w && p.y > f.H - 56) { s.sel = i; s.t = 0; s.formed = 0; return; }
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var pr = pairs[s.sel] || { a: 'NaCl', b: 'AgNO₃', solid: 'AgCl↓', note: '' };
        s.t += 1 / 60;
        var cy = (H - 56) / 2 + 6;
        // 烧杯
        ctx.strokeStyle = P.grid; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(40, 26); ctx.lineTo(40, H - 66); ctx.lineTo(W - 40, H - 66); ctx.lineTo(W - 40, 26); ctx.stroke();
        ctx.fillStyle = 'rgba(96,165,250,.16)'; ctx.fillRect(42, cy, W - 84, H - 66 - cy);
        // 离子（两种颜色），相遇后下沉形成沉淀
        var N = 26, seed = 7;
        for (var i = 0; i < N; i++) {
          seed = (seed * 16807) % 2147483647; var ux = seed / 2147483647;
          seed = (seed * 16807) % 2147483647; var uy = seed / 2147483647;
          var phase = (s.t * 0.7 + i / N) % 1;
          var isSolid = phase > 0.72;
          var px = 60 + ux * (W - 120);
          var py = isSolid ? (H - 78 - uy * 12) : (cy + 10 + uy * (H - 90 - cy));
          ctx.beginPath(); ctx.arc(px, py, isSolid ? 4.4 : 3.2, 0, Math.PI * 2);
          ctx.fillStyle = isSolid ? '#f8fafc' : (i % 2 ? '#60a5fa' : '#f59e0b');
          if (isSolid) ctx.strokeStyle = '#94a3b8', ctx.lineWidth = 1, ctx.stroke();
          ctx.fill();
        }
        h.label(ctx, pr.a + '  ' + pr.b + '  →  ' + pr.solid, W / 2, 14, P.ink, 14, 'center', '800');
        // 选择筹码
        var n = pairs.length, w = (W - 40) / Math.max(1, n);
        pairs.forEach(function (pp, i) {
          ctx.fillStyle = s.sel === i ? P.fill : 'rgba(148,163,184,.14)';
          ctx.strokeStyle = s.sel === i ? P.accent : P.grid; ctx.lineWidth = 1.8;
          h.rrect(ctx, 22 + i * w, H - 48, w - 6, 38, 9); ctx.fill(); ctx.stroke();
          h.label(ctx, pp.a + ' + ' + pp.b, 22 + i * w + (w - 6) / 2, H - 29, P.ink, 12.5, 'center', '700');
        });
        h.label(ctx, '白色颗粒下沉 = 生成沉淀', 60, H - 76, P.muted, 11.5, 'left', '600');
        this.readout(pr.a + ' 与 ' + pr.b + ' 混合：离子相互交换成分，生成' + (pr.solid.indexOf('↓') >= 0 ? '难溶的' + pr.solid.replace('↓', '') + '沉淀' : pr.solid) +
          '——这就是复分解反应发生的条件之一：有沉淀（或气体或水）生成。' + (pr.note || ''));
      }
    });
  }

  /* ---------- 26) 平仄节奏：点击/播放看长短与高低 ---------- */
  function tone(cfg) {
    var line = cfg.line || [];
    return global.TeachAnyLab.mount({
      canvas: cfg.canvas, readout: cfg.readout, cursor: 'pointer', sharedState: cfg.sharedState,
      initial: { t: 0, playing: false, at: -1 },
      onPointer: function (type, p, s) {
        if (type !== 'pointerdown') return;
        var f = this.fit(), n = line.length, w = (f.W - 60) / n;
        for (var i = 0; i < n; i++) {
          var x = 30 + i * w;
          if (p.x > x && p.x < x + w - 6 && p.y > 50 && p.y < f.H - 40) { s.playing = true; s.t = 0; s.at = i; return; }
        }
      },
      draw: function (ctx, W, H, s) {
        var P = this.palette, h = this.helpers;
        ctx.clearRect(0, 0, W, H); ctx.fillStyle = P.bg; h.rrect(ctx, 0, 0, W, H, 14); ctx.fill();
        var n = line.length, w = (W - 60) / n;
        s.t += 1 / 60;
        var beat = s.playing ? Math.floor(s.t * 2.2) % n : -1;
        var cur = (s.at >= 0 && s.playing) ? Math.floor(s.t * 2.2) % n : s.at;
        line.forEach(function (ch, i) {
          var x = 30 + i * w;
          var ping = ch.t === '平';
          var active = (i === cur);
          // 音高线：平声平直、仄声起伏
          var y = ping ? 62 : 62;
          ctx.strokeStyle = ping ? P.accent : P.accent2; ctx.lineWidth = active ? 4 : 2.4;
          ctx.beginPath();
          if (ping) { ctx.moveTo(x + 6, y); ctx.lineTo(x + w - 12, y); }
          else {
            ctx.moveTo(x + 6, y - 14); ctx.lineTo(x + w / 2, y + 12); ctx.lineTo(x + w - 12, y - 14);
          }
          ctx.stroke();
          // 时长条：平声长、仄声短
          ctx.fillStyle = ping ? 'rgba(2,132,199,.22)' : 'rgba(217,119,6,.25)';
          h.rrect(ctx, x + 4, H - 36, (w - 14) * (ping ? 0.92 : 0.55), 8, 4); ctx.fill();
          ctx.fillStyle = active ? P.fill : 'transparent';
          if (active) { h.rrect(ctx, x + 2, 40, w - 8, H - 86, 10); ctx.fill(); }
          h.label(ctx, ch.c, x + w / 2 - 4, H - 62, active ? P.accent : P.ink, 22, 'center', '800');
          h.label(ctx, ch.t, x + w / 2 - 4, H - 18, ping ? P.accent : P.accent2, 12.5, 'center', '700');
        });
        h.label(ctx, '平声：又平又长（—）　仄声：有升有降、短促（∨）', W / 2, 20, P.muted, 12, 'center', '600');
        this.readout(cur >= 0 && line[cur]
          ? '「' + line[cur].c + '」读作' + line[cur].t + '声：' + (line[cur].t === '平' ? '声音平直、可以拖长。' : '声音短促、有起伏（上声/去声/入声）。')
          : '点击任意一个字，听（看）它的平仄：一、二声是平声，三、四声是仄声；平仄交替出现，读起来就有节奏感。');
      }
    });
  }

  var SCENES = { friction: friction, pushpull: pushpull, shadow: shadow, lever: lever };
  /* 后加入的场景（magnet/moon/radar/match）在此并入注册表 */
  SCENES.magnet = magnet; SCENES.moon = moon; SCENES.radar = radar; SCENES.match = match;
  SCENES.parts = parts; SCENES.pie = pie; SCENES.ruler = ruler; SCENES.heat = heat;
  SCENES.dissolve = dissolve; SCENES.building = building; SCENES.calendar = calendar; SCENES.tree = tree;
  SCENES.heatModes = heatModes; SCENES.circleGeo = circleGeo; SCENES.proportion = proportion;
  SCENES.lineAngle = lineAngle; SCENES.rotation = rotation; SCENES.triangle = triangle;
  SCENES.timeline = timeline; SCENES.diffusion = diffusion; SCENES.lens = lens;
  SCENES.reaction = reaction; SCENES.tone = tone;

  global.TeachAnyScenes = {
    mount: function (name, cfg) {
      if (!SCENES[name]) return null;
      return SCENES[name](cfg);
    },
    has: function (name) { return !!SCENES[name]; }
  };
})(window);
