/* TeachAny Model Lab v1 — 学科真实模型互动引擎
 * 替换 zh-shell 课件的假"系统响应曲线"（通用正弦模板）。
 * 每个模型族对应一条真实学科规律；滑块调节真实变量，曲线由真实公式驱动。
 * 用法：
 *   <canvas id="modelLabCanvas" width="920" height="380"></canvas>
 *   <div id="modelLabControls"></div><p id="modelLabReadout"></p>
 *   <script src="../../assets/engines/model-lab/v1/engine.js"></script>
 *   <script>TeachAnyModelLab.mount({model:'logistic', ...})</script>
 */
(function () {
  'use strict';

  var C = {
    bg: '#081426', grid: '#24435f', axis: '#6ee7b7', curve: '#34d399',
    curve2: '#38bdf8', point: '#22d3ee', text: '#d1fae5', warn: '#fbbf24',
    shade: 'rgba(52,211,153,.10)'
  };

  function setupCanvas(cv) {
    var ctx = cv.getContext('2d');
    ctx.fillStyle = C.bg;
    ctx.fillRect(0, 0, cv.width, cv.height);
    return ctx;
  }

  function axes(ctx, cv, cfg) {
    var L = 78, R = cv.width - 40, T = 28, B = cv.height - 46;
    ctx.strokeStyle = C.grid; ctx.lineWidth = 1.4;
    ctx.fillStyle = C.axis; ctx.font = '13px sans-serif'; ctx.textAlign = 'right';
    for (var i = 0; i <= 5; i++) {
      var y = T + (B - T) * i / 5;
      ctx.beginPath(); ctx.moveTo(L, y); ctx.lineTo(R, y); ctx.stroke();
      var v = (cfg.yMax != null ? cfg.yMax : 100) * (1 - i / 5);
      ctx.fillText(formatTick(v), L - 8, y + 4);
    }
    ctx.textAlign = 'center';
    ctx.fillStyle = C.text; ctx.font = '14px sans-serif';
    ctx.fillText(cfg.xLabel || '', (L + R) / 2, cv.height - 14);
    ctx.save(); ctx.translate(18, (T + B) / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText(cfg.yLabel || '', 0, 0); ctx.restore();
    if (cfg.title) {
      ctx.textAlign = 'left'; ctx.fillStyle = C.axis; ctx.font = 'bold 15px sans-serif';
      ctx.fillText(cfg.title, L, 18);
    }
    return { L: L, R: R, T: T, B: B };
  }

  function formatTick(v) {
    if (Math.abs(v) >= 1) return String(Math.round(v));
    return v.toFixed(1);
  }

  function plot(ctx, box, fn, xMax, yMax, color, width) {
    ctx.strokeStyle = color || C.curve; ctx.lineWidth = width || 3.5;
    ctx.beginPath();
    var N = 160, started = false;
    for (var i = 0; i <= N; i++) {
      var x = xMax * i / N;
      var y = fn(x);
      if (!isFinite(y)) { started = false; continue; }
      y = Math.max(0, Math.min(yMax * 1.2, y));
      var px = box.L + (box.R - box.L) * i / N;
      var py = box.B - (box.B - box.T) * (y / yMax);
      if (!started) { ctx.moveTo(px, py); started = true; } else ctx.lineTo(px, py);
    }
    ctx.stroke();
  }

  function annotate(ctx, box, x, y, xMax, yMax, text, color) {
    var px = box.L + (box.R - box.L) * (x / xMax);
    var py = box.B - (box.B - box.T) * (y / yMax);
    ctx.fillStyle = color || C.warn;
    ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI * 2); ctx.fill();
    ctx.font = '13px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText(text, Math.min(px + 9, box.R - 90), py - 8);
  }

  function bars(ctx, box, cats, vals, yMax, colors) {
    var n = cats.length, w = (box.R - box.L) / n;
    for (var i = 0; i < n; i++) {
      var h = (box.B - box.T) * Math.max(0, vals[i]) / yMax;
      ctx.fillStyle = (colors && colors[i]) || (i % 2 ? C.curve2 : C.curve);
      ctx.globalAlpha = .85;
      ctx.fillRect(box.L + w * i + w * .18, box.B - h, w * .64, h);
      ctx.globalAlpha = 1;
      ctx.fillStyle = C.text; ctx.font = '13px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(cats[i], box.L + w * i + w / 2, box.B + 18);
      ctx.fillStyle = C.axis;
      ctx.fillText(formatTick(vals[i]), box.L + w * i + w / 2, box.B - h - 8);
    }
  }

  /* ---------------- 模型族：每族 {render(ctx,cv,cfg,v), readout(cfg,v)} ---------------- */

  var MODELS = {
    /* 钟形曲线：酶活性-温度/pH。滑块：环境温度(x轴指针)、最适点偏移 */
    bell: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var opt = v.opt != null ? v.opt : (cfg.params.opt || 37);
        var width = cfg.params.width || 12;
        plot(ctx, box, function (x) {
          var d = (x - opt) / width;
          return 100 * Math.exp(-d * d);
        }, cfg.xMax, 100);
        if (v.env != null) {
          var d = (v.env - opt) / width;
          annotate(ctx, box, v.env, 100 * Math.exp(-d * d), cfg.xMax, 100,
            '当前活性 ' + Math.round(100 * Math.exp(-d * d)) + '%', C.warn);
        }
        annotate(ctx, box, opt, 100, cfg.xMax, 100, '最适' + (cfg.params.optName || '条件'), C.point);
      },
      readout: function (cfg, v) {
        var opt = v.opt != null ? v.opt : cfg.params.opt;
        var d = (v.env - opt) / (cfg.params.width || 12);
        var act = Math.round(100 * Math.exp(-d * d));
        return '当前' + cfg.sliders[0].label + ' ' + v.env + cfg.unit0 + ' → 相对活性 ' + act + '%。' + cfg.explain;
      }
    },

    /* 饱和曲线：光合速率-光强、跨膜运输、酶促反应 v=Vmax·x/(Km+x) */
    saturate: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var vmax = v.vmax != null ? v.vmax : cfg.params.vmax;
        var km = cfg.params.km || cfg.xMax / 4;
        plot(ctx, box, function (x) { return vmax * x / (km + x); }, cfg.xMax, cfg.yMax);
        if (cfg.params.compareLinear) {
          plot(ctx, box, function (x) { return cfg.params.linearK * x; }, cfg.xMax, cfg.yMax, C.curve2, 2.5);
        }
        if (cfg.params.flat != null) {
          plot(ctx, box, function () { return cfg.params.flat; }, cfg.xMax, cfg.yMax, C.curve2, 2.5);
          ctx.fillStyle = C.curve2; ctx.font = '13px sans-serif'; ctx.textAlign = 'left';
          ctx.fillText('— ' + (cfg.params.flatName || '对照'), box.L + 10, box.T + 34);
        }
        annotate(ctx, box, km, vmax / 2, cfg.xMax, cfg.yMax, cfg.params.kmName || '半饱和点', C.warn);
      },
      readout: function (cfg, v) {
        var vmax = v.vmax != null ? v.vmax : cfg.params.vmax;
        return cfg.explain.replace('{vmax}', Math.round(vmax));
      }
    },

    /* logistic S 型增长：种群。滑块：r、K */
    logistic: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var r = v.r != null ? v.r : .5, K = v.K != null ? v.K : 100;
        var N0 = cfg.params.n0 || 4;
        plot(ctx, box, function (t) {
          return K / (1 + ((K - N0) / N0) * Math.exp(-r * t));
        }, cfg.xMax, cfg.yMax);
        /* K 线 */
        ctx.strokeStyle = C.warn; ctx.setLineDash([6, 5]); ctx.lineWidth = 1.6;
        var ky = box.B - (box.B - box.T) * (K / cfg.yMax);
        ctx.beginPath(); ctx.moveTo(box.L, ky); ctx.lineTo(box.R, ky); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = C.warn; ctx.font = '13px sans-serif'; ctx.textAlign = 'left';
        ctx.fillText('K = ' + Math.round(K), box.R - 90, ky - 6);
        annotate(ctx, box, cfg.params.halfTime != null ? cfg.params.halfTime : Math.log((K - N0) / N0) / r,
          K / 2, cfg.xMax, cfg.yMax, 'K/2 增长最快', C.point);
      },
      readout: function (cfg, v) {
        var r = v.r != null ? v.r : .5, K = v.K != null ? v.K : 100;
        return 'r=' + r.toFixed(2) + '，K=' + Math.round(K) + '：' + cfg.explain;
      }
    },

    /* 捕食者-猎物振荡（Lotka-Volterra 数值积分） */
    oscillate: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var a = .1, b = .002, c = .05, d = .001;
        var prey0 = v.prey != null ? v.prey : 40, pred0 = v.pred != null ? v.pred : 10;
        var dt = .5, steps = Math.round(cfg.xMax / dt);
        var prey = [prey0], pred = [pred0];
        for (var i = 1; i <= steps; i++) {
          var P = prey[i - 1], Q = pred[i - 1];
          prey.push(Math.max(0, P + (a * P - b * P * Q) * dt * 10));
          pred.push(Math.max(0, Q + (d * P * Q - c * Q) * dt * 10));
        }
        var yMax = cfg.yMax;
        plot(ctx, box, function (t) { return prey[Math.min(steps, Math.round(t / dt))]; }, cfg.xMax, yMax, C.curve, 3);
        plot(ctx, box, function (t) { return pred[Math.min(steps, Math.round(t / dt))]; }, cfg.xMax, yMax, C.curve2, 3);
        ctx.fillStyle = C.curve; ctx.font = '13px sans-serif'; ctx.textAlign = 'left';
        ctx.fillText('— ' + (cfg.params.preyName || '猎物'), box.L + 10, box.T + 16);
        ctx.fillStyle = C.curve2;
        ctx.fillText('— ' + (cfg.params.predName || '捕食者'), box.L + 10, box.T + 34);
      },
      readout: function (cfg, v) { return cfg.explain; }
    },

    /* 负反馈调节：血糖/体温/甲状腺激素。滑块：扰动强度、反馈灵敏度 */
    feedback: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var set = cfg.params.setpoint || 50;
        var shock = v.shock != null ? v.shock : 30;
        var sens = v.sens != null ? v.sens : .5;
        /* 正常参考带 */
        ctx.fillStyle = C.shade;
        var y1 = box.B - (box.B - box.T) * ((set * 1.1) / cfg.yMax);
        var y2 = box.B - (box.B - box.T) * ((set * .9) / cfg.yMax);
        ctx.fillRect(box.L, y1, box.R - box.L, y2 - y1);
        ctx.fillStyle = C.axis; ctx.font = '12px sans-serif'; ctx.textAlign = 'left';
        ctx.fillText('正常范围', box.L + 6, y1 + 14);
        plot(ctx, box, function (t) {
          return set + shock * Math.exp(-sens * t / (cfg.xMax / 6)) * Math.cos(t / (cfg.xMax / 8));
        }, cfg.xMax, cfg.yMax);
      },
      readout: function (cfg, v) {
        var sens = v.sens != null ? v.sens : .5;
        var t = (cfg.xMax / 6) / sens;
        return '扰动 +' + (v.shock != null ? v.shock : 30) + '，反馈灵敏度 ' + sens.toFixed(2) +
          ' → 约 ' + t.toFixed(1) + ' ' + (cfg.timeUnit || '单位时间') + '回到正常范围。' + cfg.explain;
      }
    },

    /* 能量金字塔：滑块传递效率 10-20% */
    pyramid: {
      render: function (ctx, cv, cfg, v) {
        var eff = (v.eff != null ? v.eff : 15) / 100;
        var levels = cfg.params.levels || ['生产者', '初级消费者', '次级消费者', '三级消费者'];
        var base = cfg.params.base || 10000;
        var box = axes(ctx, cv, cfg);
        var n = levels.length, layerH = (box.B - box.T) / n;
        var maxW = (box.R - box.L) * .8, cx = (box.L + box.R) / 2;
        for (var i = 0; i < n; i++) {
          var e1 = base * Math.pow(eff, i), e2 = base * Math.pow(eff, i + 1);
          var w1 = maxW * Math.sqrt(e1 / base), w2 = maxW * Math.sqrt(e2 / base);
          var y1 = box.B - layerH * i, y2 = box.B - layerH * (i + 1);
          ctx.beginPath();
          ctx.moveTo(cx - w1 / 2, y1); ctx.lineTo(cx + w1 / 2, y1);
          ctx.lineTo(cx + w2 / 2, y2); ctx.lineTo(cx - w2 / 2, y2);
          ctx.closePath();
          ctx.fillStyle = 'rgba(52,211,153,' + (0.55 - i * .1) + ')'; ctx.fill();
          ctx.strokeStyle = C.curve; ctx.lineWidth = 1.5; ctx.stroke();
          ctx.fillStyle = C.text; ctx.font = '13px sans-serif'; ctx.textAlign = 'center';
          ctx.fillText(levels[i] + '  ' + Math.round(e1), cx, (y1 + y2) / 2 + 4);
        }
      },
      readout: function (cfg, v) {
        var eff = v.eff != null ? v.eff : 15;
        var top = Math.round((cfg.params.base || 10000) * Math.pow(eff / 100, (cfg.params.levels || [1, 2, 3, 4]).length - 1));
        return '传递效率 ' + eff + '%：顶级消费者只得到约 ' + top + ' 单位能量。' + cfg.explain;
      }
    },

    /* 比例柱状：遗传比例、时相占比、放射性分布。滑块改参数重算 vals */
    bars: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var vals = cfg.compute(v);
        bars(ctx, box, cfg.params.cats, vals, cfg.yMax || Math.max.apply(null, vals) * 1.25, cfg.params.colors);
      },
      readout: function (cfg, v) { return cfg.computeReadout(v); }
    },

    /* 有丝分裂：染色体数/DNA 数阶梯折线 */
    steps: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var phases = cfg.params.phases; /* [{name, dna, chr}] */
        var showDNA = v.series == null ? true : !!v.series;
        var xMax = phases.length;
        function valAt(i, key) { return phases[Math.min(phases.length - 1, Math.floor(i))][key]; }
        ctx.lineWidth = 3;
        [showDNA ? 'dna' : 'chr'].forEach(function (key, idx) {
          ctx.strokeStyle = idx ? C.curve2 : C.curve;
          ctx.beginPath();
          for (var s = 0; s < phases.length; s++) {
            var x1 = box.L + (box.R - box.L) * s / xMax;
            var x2 = box.L + (box.R - box.L) * (s + 1) / xMax;
            var y = box.B - (box.B - box.T) * (phases[s][key] / cfg.yMax);
            if (s === 0) ctx.moveTo(x1, y); else ctx.lineTo(x1, y);
            ctx.lineTo(x2, y);
          }
          ctx.stroke();
        });
        ctx.fillStyle = C.text; ctx.font = '13px sans-serif'; ctx.textAlign = 'center';
        phases.forEach(function (p, s) {
          ctx.fillText(p.name, box.L + (box.R - box.L) * (s + .5) / xMax, box.B + 18);
        });
        ctx.textAlign = 'left';
        ctx.fillStyle = C.curve; ctx.fillText('— DNA 数', box.L + 10, box.T + 16);
      },
      readout: function (cfg, v) { return cfg.explain; }
    },

    /* 指数衰减：端粒/信号扩散 y = y0·e^(-kx)，滑块 k 或 y0 */
    decay: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var k = v.k != null ? v.k : .5, y0 = cfg.params.y0 || 100;
        plot(ctx, box, function (x) { return y0 * Math.exp(-k * x / (cfg.xMax / 3)); }, cfg.xMax, cfg.yMax);
        var half = Math.LN2 * (cfg.xMax / 3) / k;
        annotate(ctx, box, half, y0 / 2, cfg.xMax, cfg.yMax, (cfg.params.halfName || '半衰点') + '≈' + half.toFixed(1), C.warn);
      },
      readout: function (cfg, v) {
        var k = v.k != null ? v.k : .5;
        return cfg.explain.replace('{half}', (Math.LN2 * (cfg.xMax / 3) / k).toFixed(1));
      }
    },

    /* 真实数据散点 + 趋势：进化分子证据等 */
    points: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var pts = cfg.params.points; /* [{x,y,label}] */
        /* 趋势线 */
        var n = pts.length, sx = 0, sy = 0, sxy = 0, sxx = 0;
        pts.forEach(function (p) { sx += p.x; sy += p.y; sxy += p.x * p.y; sxx += p.x * p.x; });
        var slope = (n * sxy - sx * sy) / (n * sxx - sx * sx);
        var intercept = (sy - slope * sx) / n;
        plot(ctx, box, function (x) { return Math.max(0, slope * x + intercept); }, cfg.xMax, cfg.yMax, C.grid, 2);
        var showAll = v.detail != null ? !!v.detail : false;
        pts.forEach(function (p, i) {
          if (!showAll && i % 2) return;
          annotate(ctx, box, p.x, p.y, cfg.xMax, cfg.yMax, p.label, C.point);
        });
      },
      readout: function (cfg, v) { return cfg.explain; }
    },

    /* 算法复杂度：滑块 n，画 n² / n·log n / log n */
    complexity: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var xMax = cfg.xMax;
        var yMax = cfg.yMax;
        plot(ctx, box, function (n) { return n * n / 10; }, xMax, yMax, '#f87171', 2.5);
        plot(ctx, box, function (n) { return n * Math.log2(n + 1); }, xMax, yMax, C.curve, 3);
        plot(ctx, box, function (n) { return n; }, xMax, yMax, C.curve2, 2.5);
        plot(ctx, box, function (n) { return Math.log2(n + 1) * 10; }, xMax, yMax, C.warn, 2.5);
        var lg = [['#f87171', 'n²/10 冒泡类排序'], [C.curve, 'n·log n 快排/归并'], [C.curve2, 'n 顺序查找'], [C.warn, '10·log n 二分查找']];
        ctx.font = '13px sans-serif'; ctx.textAlign = 'left';
        lg.forEach(function (t, i) {
          ctx.fillStyle = t[0];
          ctx.fillText('— ' + t[1], box.L + 10, box.T + 16 + i * 18);
        });
        var n = v.n != null ? v.n : 50;
        annotate(ctx, box, n, n * Math.log2(n + 1), xMax, yMax, 'n=' + n, C.point);
      },
      readout: function (cfg, v) {
        var n = v.n != null ? v.n : 50;
        return 'n=' + n + '：冒泡约 ' + Math.round(n * n / 2) + ' 次比较，快排约 ' + Math.round(n * Math.log2(n)) +
          ' 次，二分查找最多 ' + Math.ceil(Math.log2(n + 1)) + ' 次。' + cfg.explain;
      }
    },

    /* 生长素两重性：对数浓度轴，低促高抑 */
    hormone: {
      render: function (ctx, cv, cfg, v) {
        var box = axes(ctx, cv, cfg);
        var zero = box.T + (box.B - box.T) * .45;
        ctx.strokeStyle = C.grid; ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.moveTo(box.L, zero); ctx.lineTo(box.R, zero); ctx.stroke();
        ctx.fillStyle = C.text; ctx.font = '12px sans-serif'; ctx.textAlign = 'left';
        ctx.fillText('促进', box.L + 6, zero - 8);
        ctx.fillText('抑制', box.L + 6, zero + 16);
        var opt = v.opt != null ? v.opt : 4;
        ctx.strokeStyle = C.curve; ctx.lineWidth = 3.5; ctx.beginPath();
        for (var i = 0; i <= 160; i++) {
          var lx = i / 160 * 8; /* log 浓度 10^-8..1 */
          var g = Math.exp(-Math.pow((lx - opt) / 1.6, 2)) * 1.3 - Math.exp(-Math.pow((lx - 7.6) / 1.1, 2)) * .9;
          var px = box.L + (box.R - box.L) * i / 160;
          var py = zero - g * (box.B - box.T) * .38;
          if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.fillStyle = C.text; ctx.font = '13px sans-serif'; ctx.textAlign = 'center';
        ['10⁻⁸', '10⁻⁶', '10⁻⁴', '10⁻²', '1'].forEach(function (t, i) {
          ctx.fillText(t, box.L + (box.R - box.L) * i / 4, box.B + 18);
        });
        ctx.fillText('生长素浓度 (mol/L)', (box.L + box.R) / 2, box.B + 38);
      },
      readout: function (cfg, v) {
        return '最适浓度约 10⁻' + (v.opt != null ? Math.round(v.opt) : 4) + ' mol/L：低于它促进，远高于它抑制。' + cfg.explain;
      }
    },

    /* DNA 半保留复制：代数滑块，杂合/轻型比例 */
    replication: {
      render: function (ctx, cv, cfg, v) {
        var gen = Math.max(0, Math.min(4, Math.round(v.gen != null ? v.gen : 2)));
        var box = axes(ctx, cv, cfg);
        var hybrid = gen === 0 ? 0 : 2 / Math.pow(2, gen);
        var light = gen === 0 ? 0 : 1 - hybrid;
        var heavy = gen === 0 ? 1 : 0;
        bars(ctx, box, ['¹⁵N 重链', '杂合 ¹⁴N/¹⁵N', '¹⁴N 轻链'],
          [heavy * 100, hybrid * 100, light * 100], 110,
          ['#f87171', C.warn, C.curve]);
        ctx.fillStyle = C.text; ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'left';
        ctx.fillText('第 ' + gen + ' 代（共 ' + Math.pow(2, gen) + ' 个 DNA 分子）', box.L + 10, box.T + 16);
      },
      readout: function (cfg, v) {
        var gen = Math.max(0, Math.min(4, Math.round(v.gen != null ? v.gen : 2)));
        if (gen === 0) return '第 0 代：所有 DNA 都是 ¹⁵N 重链。' + cfg.explain;
        return '第 ' + gen + ' 代：杂合 DNA 占 2/' + Math.pow(2, gen) + '，其余为轻链。这正是半保留复制的证据。' + cfg.explain;
      }
    },

    /* 孟德尔杂交：样本量滑块，观察比例收敛到大数定律 */
    mendel: {
      render: function (ctx, cv, cfg, v) {
        var n = v.n != null ? v.n : 40;
        var box = axes(ctx, cv, cfg);
        /* 用确定性伪随机（种子=n）演示比例随样本量收敛 */
        var ratio = cfg.params.ratio || [3, 1];
        var total = ratio[0] + ratio[1];
        var expect = ratio[0] / total;
        var counts = [0, 0];
        var seed = n * 2654435761 % 2147483647;
        for (var i = 0; i < n; i++) {
          seed = (seed * 48271) % 2147483647;
          if (seed / 2147483647 < expect) counts[0]++; else counts[1]++;
        }
        var cats = cfg.params.cats;
        bars(ctx, box, cats, [counts[0] / n * 100, counts[1] / n * 100], 110, [C.curve, C.curve2]);
        /* 理论线 */
        ctx.strokeStyle = C.warn; ctx.setLineDash([6, 5]); ctx.lineWidth = 1.6;
        var ty = box.B - (box.B - box.T) * (expect * 100 / 110);
        ctx.beginPath(); ctx.moveTo(box.L, ty); ctx.lineTo(box.R, ty); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = C.warn; ctx.font = '13px sans-serif'; ctx.textAlign = 'left';
        ctx.fillText('理论 ' + (expect * 100).toFixed(0) + '%', box.R - 110, ty - 6);
      },
      readout: function (cfg, v) {
        var n = v.n != null ? v.n : 40;
        return '样本量 ' + n + '：' + cfg.explain;
      }
    }
  };

  /* ---------------- 挂载 ---------------- */

  function mount(cfg) {
    var cv = document.getElementById(cfg.canvasId || 'modelLabCanvas');
    var controls = document.getElementById(cfg.controlsId || 'modelLabControls');
    var readout = document.getElementById(cfg.readoutId || 'modelLabReadout');
    if (!cv || !MODELS[cfg.model]) return;
    var values = {};
    (cfg.sliders || []).forEach(function (s) { values[s.key] = s.value; });

    function redraw() {
      var ctx = setupCanvas(cv);
      MODELS[cfg.model].render(ctx, cv, cfg, values);
      if (readout && MODELS[cfg.model].readout) {
        readout.textContent = MODELS[cfg.model].readout(cfg, values);
      }
    }

    if (controls) {
      controls.innerHTML = '';
      (cfg.sliders || []).forEach(function (s) {
        var label = document.createElement('label');
        label.style.cssText = 'display:inline-flex;align-items:center;gap:8px;margin:6px 14px 6px 0;font-size:14px;';
        var input = document.createElement('input');
        input.type = 'range'; input.min = s.min; input.max = s.max;
        input.value = s.value; input.step = s.step || 1;
        var val = document.createElement('strong');
        val.textContent = s.value + (s.unit || '');
        input.addEventListener('input', function () {
          values[s.key] = parseFloat(input.value);
          val.textContent = input.value + (s.unit || '');
          redraw();
        });
        label.appendChild(document.createTextNode(s.label + ' '));
        label.appendChild(input);
        label.appendChild(val);
        controls.appendChild(label);
      });
      var reset = document.createElement('button');
      reset.textContent = '重置';
      reset.style.cssText = 'padding:6px 16px;border-radius:8px;border:1px solid rgba(148,163,184,.35);background:rgba(51,65,85,.55);color:inherit;cursor:pointer;';
      reset.addEventListener('click', function () {
        (cfg.sliders || []).forEach(function (s, i) {
          values[s.key] = s.value;
          controls.querySelectorAll('input[type=range]')[i].value = s.value;
          controls.querySelectorAll('strong')[i].textContent = s.value + (s.unit || '');
        });
        redraw();
      });
      controls.appendChild(reset);
    }
    redraw();
  }

  window.TeachAnyModelLab = { mount: mount, version: '1.0.0' };
})();
