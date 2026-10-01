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

  var SCENES = { friction: friction, pushpull: pushpull, shadow: shadow, lever: lever };
  /* 后加入的场景（magnet/moon/radar/match）在此并入注册表 */
  SCENES.magnet = magnet; SCENES.moon = moon; SCENES.radar = radar; SCENES.match = match;

  global.TeachAnyScenes = {
    mount: function (name, cfg) {
      if (!SCENES[name]) return null;
      return SCENES[name](cfg);
    },
    has: function (name) { return !!SCENES[name]; }
  };
})(window);
