/* 信号与处理 PBL · 教学实验台（采样 / 卷积 / 频谱 / 滤波 / 听音 / 问题板） */
(function () {
  'use strict';

  const TAU = Math.PI * 2;

  function $(id) { return document.getElementById(id); }
  function setText(id, text) { const el = $(id); if (el) el.textContent = text; }

  function drawGrid(ctx, w, h, y0) {
    ctx.save();
    ctx.strokeStyle = 'rgba(148,163,184,0.18)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, y0); ctx.lineTo(w, y0);
    ctx.stroke();
    ctx.restore();
  }

  function plotPolyline(ctx, xs, ys, color, width) {
    ctx.beginPath();
    xs.forEach((x, i) => {
      if (i === 0) ctx.moveTo(x, ys[i]);
      else ctx.lineTo(x, ys[i]);
    });
    ctx.strokeStyle = color;
    ctx.lineWidth = width || 2;
    ctx.stroke();
  }

  /* ───────── Web Audio 对照听音 ───────── */
  let audioCtx = null;
  let currentNodes = [];

  function ensureAudio() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    return audioCtx;
  }

  function stopAudio() {
    currentNodes.forEach((n) => { try { n.stop?.(); n.disconnect?.(); } catch (e) {} });
    currentNodes = [];
  }

  function playVersion(kind) {
    const ctx = ensureAudio();
    stopAudio();
    const dur = 2.4;
    const t0 = ctx.currentTime + 0.02;
    const master = ctx.createGain();
    master.gain.value = 0.22;
    master.connect(ctx.destination);

    function tone(freq, amp, type) {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = type || 'sine';
      o.frequency.value = freq;
      g.gain.value = amp;
      o.connect(g); g.connect(master);
      o.start(t0); o.stop(t0 + dur);
      currentNodes.push(o);
      return g;
    }

    // 语音近似：基频 + 谐波（齿音用较高谐波）
    const speech = () => {
      tone(180, 0.35); tone(360, 0.22); tone(540, 0.12);
      tone(2200, 0.08); tone(3200, 0.05);
    };
    const hum = () => tone(50, 0.18);
    const noise = (amp) => {
      const len = Math.floor(ctx.sampleRate * dur);
      const buf = ctx.createBuffer(1, len, ctx.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < len; i++) data[i] = (Math.random() * 2 - 1) * amp;
      const src = ctx.createBufferSource();
      src.buffer = buf;
      const g = ctx.createGain();
      g.gain.value = 1;
      src.connect(g); g.connect(master);
      src.start(t0); src.stop(t0 + dur);
      currentNodes.push(src);
    };

    let note = '';
    if (kind === 'A') {
      speech(); hum(); noise(0.22);
      note = 'A 现场：语音 + 50 Hz 哼声 + 宽带噪声。听不清，但信息还在。';
    } else if (kind === 'B') {
      speech(); hum(); noise(0.22);
      master.gain.value = 0.85;
      const clip = ctx.createWaveShaper();
      const curve = new Float32Array(256);
      for (let i = 0; i < 256; i++) {
        const x = i / 128 - 1;
        curve[i] = Math.max(-0.4, Math.min(0.4, x * 3));
      }
      clip.curve = curve;
      master.disconnect();
      master.connect(clip); clip.connect(ctx.destination);
      note = 'B 只放大：削波引入谐波。更响，齿音被噪声和谐波盖住。非线性已破坏叠加性。';
    } else if (kind === 'C') {
      speech(); hum(); noise(0.12);
      const lp = ctx.createBiquadFilter();
      lp.type = 'lowpass'; lp.frequency.value = 700; lp.Q.value = 0.7;
      master.disconnect();
      master.connect(lp); lp.connect(ctx.destination);
      note = 'C 错误低通：700 Hz 截止切掉辅音频带。听起来更「电话音」，可懂度下降。';
    } else {
      speech();
      const hp = ctx.createBiquadFilter();
      hp.type = 'highpass'; hp.frequency.value = 80;
      const notch = ctx.createBiquadFilter();
      notch.type = 'notch'; notch.frequency.value = 50; notch.Q.value = 12;
      master.gain.value = 0.28;
      master.disconnect();
      master.connect(hp); hp.connect(notch); notch.connect(ctx.destination);
      note = 'D 对照：抑制哼声、保留 2–3 kHz 辅音区。仍是 LTI 链路，不是魔法降噪。';
    }
    setText('listen-feedback', note);
  }

  document.querySelectorAll('[data-listen]').forEach((btn) => {
    btn.addEventListener('click', () => playVersion(btn.getAttribute('data-listen')));
  });
  $('btn-stop-audio')?.addEventListener('click', stopAudio);

  /* ───────── 问题板 L1–L3 ───────── */
  const BOARD_KEY = 'info-u-signals-pbl-board';

  function loadBoard() {
    try { return JSON.parse(localStorage.getItem(BOARD_KEY) || '[]'); } catch (e) { return []; }
  }
  function saveBoard(items) { localStorage.setItem(BOARD_KEY, JSON.stringify(items)); }

  function renderBoard() {
    const host = $('q-board');
    if (!host) return;
    const items = loadBoard();
    if (!items.length) {
      host.innerHTML = '<p style="color:var(--muted);margin:0">还没有问题。先听 A–D，再把困惑写成可检验命题。</p>';
      return;
    }
    host.innerHTML = items.map((it, i) => `
      <div class="q-chip q-${it.level}">
        <span class="q-lv">${it.level}</span>
        <span>${it.text}</span>
        <button type="button" data-del="${i}" aria-label="删除">×</button>
      </div>`).join('');
    host.querySelectorAll('[data-del]').forEach((b) => {
      b.addEventListener('click', () => {
        const next = loadBoard();
        next.splice(Number(b.getAttribute('data-del')), 1);
        saveBoard(next); renderBoard();
      });
    });
  }

  function addQuestion() {
    const text = ($('q-input')?.value || '').trim();
    const level = $('q-level')?.value || 'L1';
    if (!text) { setText('q-board-fb', '先写下一句问题。'); return; }
    const tips = {
      L1: '现象层。试着改成：哪个变量变了？听感差在频段还是幅度？',
      L2: '机制层。下一步：怎样用一次对照实验检验这个机制？',
      L3: '可检验。很好——把它钉到班级问题板，本周只攻这一条。'
    };
    const items = loadBoard();
    items.push({ text, level, t: Date.now() });
    saveBoard(items);
    renderBoard();
    setText('q-board-fb', tips[level] || '');
    if ($('q-input')) $('q-input').value = '';
    if (level === 'L3') window.__TEACHANY_LEARNER_QUESTION__ = text;
  }

  $('btn-add-q')?.addEventListener('click', addQuestion);
  renderBoard();

  document.querySelectorAll('[data-upgrade-demo]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const map = {
        1: 'L1→L3：为什么更响更糊？ → 若只提高增益并出现削波，频谱上 2 kHz 以上谐波是否增加、辅音可懂度是否下降？',
        2: 'L1→L3：那条横线是什么？ → 若它对应 50 Hz 工频，陷波 Q=12 后该线应消失，语音 300–3400 Hz 能量应基本不变。',
        3: 'L1→L3：怎样算更好？ → 同一测试句，SNR 与音节正确率是否同时上升，且群延迟不超过 20 ms？'
      };
      setText('upgrade-demo-fb', map[btn.getAttribute('data-upgrade-demo')] || '');
    });
  });

  /* ───────── 采样实验台 ───────── */
  function samplingLab() {
    const canvas = $('cv-sample');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const fsEl = $('sl-fs');
    const fEl = $('sl-f');
    const aaEl = $('chk-aa');

    function render() {
      const w = canvas.width, h = canvas.height;
      ctx.fillStyle = '#0b1628'; ctx.fillRect(0, 0, w, h);
      const fs = Number(fsEl?.value || 8000);
      const f = Number(fEl?.value || 2200);
      const useAA = !!aaEl?.checked;
      const nyq = fs / 2;
      const fEff = useAA && f > nyq ? 0 : f;
      const aliasK = Math.round(f / fs);
      let fAlias = Math.abs(f - aliasK * fs);
      if (fAlias > nyq) fAlias = Math.abs(fs - fAlias);
      const heard = (useAA && f > nyq) ? 0 : (f > nyq ? fAlias : f);

      const y0 = h * 0.42;
      const y1 = h * 0.82;
      drawGrid(ctx, w, h, y0);
      drawGrid(ctx, w, h, y1);

      const T = 0.008;
      const cont = [], xs = [];
      for (let i = 0; i < w; i++) {
        const t = (i / w) * T;
        xs.push(i);
        const aaGain = useAA ? 1 / (1 + Math.pow(f / Math.max(nyq, 1), 8)) : 1;
        cont.push(y0 - Math.sin(TAU * f * t) * 48 * aaGain);
      }
      plotPolyline(ctx, xs, cont, 'rgba(56,189,248,0.85)', 2);

      const nSamp = Math.max(4, Math.floor(fs * T));
      ctx.fillStyle = '#34d399';
      for (let n = 0; n < nSamp; n++) {
        const t = n / fs;
        const x = (t / T) * w;
        const aaGain = useAA ? 1 / (1 + Math.pow(f / Math.max(nyq, 1), 8)) : 1;
        const y = y0 - Math.sin(TAU * f * t) * 48 * aaGain;
        ctx.beginPath(); ctx.arc(x, y, 3.2, 0, TAU); ctx.fill();
      }

      const rec = [];
      for (let i = 0; i < w; i++) {
        const t = (i / w) * T;
        rec.push(y1 - Math.sin(TAU * heard * t) * 40);
      }
      plotPolyline(ctx, xs, rec, heard === 0 ? '#64748b' : '#a78bfa', 2);

      ctx.fillStyle = '#9fb4cc';
      ctx.font = '13px ui-sans-serif, system-ui';
      ctx.fillText('连续 / 采样点', 12, 20);
      ctx.fillText('你听到的重建（理想）', 12, y1 - 52);
      const ok = f < nyq;
      setText('sample-readout',
        `f = ${f} Hz，fs = ${fs} Hz，Nyquist = ${nyq} Hz。` +
        (ok
          ? '满足 fs > 2f，重建频率等于原频率。'
          : (useAA
            ? '已抗混叠：超过 Nyquist 的分量被压掉，重建接近静音/残差。'
            : `欠采样：重建频率 ≈ ${heard.toFixed(0)} Hz（混叠），不是 ${f} Hz。`)));
      const meter = $('sample-meter');
      if (meter) meter.textContent = ok ? '未混叠' : (useAA ? '被抗混叠抑制' : '已混叠');
      if (meter) meter.dataset.state = ok ? 'ok' : (useAA ? 'warn' : 'bad');
    }

    ['input', 'change'].forEach((ev) => {
      fsEl?.addEventListener(ev, render);
      fEl?.addEventListener(ev, render);
      aaEl?.addEventListener(ev, render);
    });
    render();
  }
  samplingLab();

  /* ───────── 卷积 / LTI ───────── */
  function convLab() {
    const canvas = $('cv-conv');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const kindEl = $('sel-h');

    function conv(x, h) {
      const y = new Array(x.length + h.length - 1).fill(0);
      for (let n = 0; n < y.length; n++) {
        let s = 0;
        for (let k = 0; k < h.length; k++) {
          const i = n - k;
          if (i >= 0 && i < x.length) s += x[i] * h[k];
        }
        y[n] = s;
      }
      return y;
    }

    function drawSeq(seq, yBase, color, label) {
      const max = Math.max(1e-6, ...seq.map(Math.abs));
      ctx.fillStyle = '#9fb4cc';
      ctx.font = '12px ui-sans-serif';
      ctx.fillText(label, 8, yBase - 36);
      seq.forEach((v, i) => {
        const x = 28 + i * 18;
        const mag = (v / max) * 40;
        ctx.strokeStyle = color;
        ctx.beginPath();
        ctx.moveTo(x, yBase);
        ctx.lineTo(x, yBase - mag);
        ctx.stroke();
        ctx.fillStyle = color;
        ctx.beginPath(); ctx.arc(x, yBase - mag, 3, 0, TAU); ctx.fill();
      });
    }

    function render() {
      const w = canvas.width, h = canvas.height;
      ctx.fillStyle = '#0b1628'; ctx.fillRect(0, 0, w, h);
      const x = [0, 0, 1, 0, 0, 0.6, 0, 0, 0, 0];
      let hImp;
      const kind = kindEl?.value || 'ma';
      if (kind === 'ma') hImp = [0.25, 0.5, 0.25];
      else if (kind === 'exp') hImp = [0.5, 0.25, 0.125, 0.06];
      else hImp = [1, -1];
      const y = conv(x, hImp);
      drawSeq(x, 70, '#38bdf8', 'x[n] 输入');
      drawSeq(hImp, 170, '#34d399', 'h[n] 冲激响应');
      drawSeq(y, 300, '#a78bfa', 'y = x * h');

      const x2 = x.map((v) => v * 2);
      const y2 = conv(x2, hImp);
      const lin = y2.every((v, i) => Math.abs(v - 2 * (y[i] || 0)) < 1e-9);
      setText('conv-readout',
        `当前 h 是 ${kind === 'ma' ? '三点滑动平均（低通 FIR）' : kind === 'exp' ? '指数衰减（IIR 截断）' : '差分器（高通）'}。` +
        `线性检验 2x → 2y：${lin ? '通过，这是线性卷积。' : '失败。'} 时不变：把 x 右移，y 同样右移。`);
    }
    kindEl?.addEventListener('change', render);
    $('btn-lin-test')?.addEventListener('click', () => {
      setText('conv-readout', '若对削波器做同样检验：2x 的输出 ≠ 2·y。B 版本「开大音量」不是 LTI，卷积公式不适用。');
    });
    render();
  }
  convLab();

  /* ───────── DFT / 窗 ───────── */
  function dftMag(x) {
    const N = x.length;
    const mag = new Array(N / 2);
    for (let k = 0; k < N / 2; k++) {
      let re = 0, im = 0;
      for (let n = 0; n < N; n++) {
        const ang = -TAU * k * n / N;
        re += x[n] * Math.cos(ang);
        im += x[n] * Math.sin(ang);
      }
      mag[k] = Math.sqrt(re * re + im * im) / N;
    }
    return mag;
  }

  function spectrumLab() {
    const canvas = $('cv-spec');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function render() {
      const N = Number($('sl-n')?.value || 128);
      const win = $('sel-win')?.value || 'hann';
      const f0 = Number($('sl-spec-f')?.value || 50);
      const fs = 2000;
      const x = new Array(N);
      for (let n = 0; n < N; n++) {
        const t = n / fs;
        const w = win === 'rect' ? 1 : 0.5 * (1 - Math.cos(TAU * n / (N - 1)));
        x[n] = w * (Math.sin(TAU * f0 * t) + 0.35 * Math.sin(TAU * 180 * t));
      }
      const mag = dftMag(x);
      const w = canvas.width, h = canvas.height;
      ctx.fillStyle = '#0b1628'; ctx.fillRect(0, 0, w, h);
      const max = Math.max(...mag, 1e-9);
      ctx.beginPath();
      mag.forEach((v, k) => {
        const xpx = (k / (mag.length - 1)) * (w - 24) + 12;
        const ypx = h - 16 - (v / max) * (h - 36);
        if (k === 0) ctx.moveTo(xpx, ypx); else ctx.lineTo(xpx, ypx);
      });
      ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2; ctx.stroke();
      const df = fs / N;
      const kTrue = Math.round(f0 / df);
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect((kTrue / (mag.length - 1)) * (w - 24) + 10, 8, 3, h - 24);
      setText('spec-readout',
        `Δf = fs/N = ${df.toFixed(2)} Hz。观测时长 T=N/fs=${(N / fs * 1000).toFixed(1)} ms。` +
        (win === 'rect'
          ? '矩形窗主瓣最窄，旁瓣高，50 Hz 与 180 Hz 容易泄漏互扰。'
          : 'Hann 旁瓣低、主瓣变宽。峰更「胖」，泄漏更小。零填充只会让谱线更密，不减小 Δf。'));
    }
    ['sl-n', 'sel-win', 'sl-spec-f'].forEach((id) => {
      $(id)?.addEventListener('input', render);
      $(id)?.addEventListener('change', render);
    });
    render();
  }
  spectrumLab();

  /* ───────── 滤波 ───────── */
  function filterLab() {
    const canvas = $('cv-filt');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function firMA(x, m) {
      const h = Array(m).fill(1 / m);
      const y = new Array(x.length).fill(0);
      for (let n = 0; n < x.length; n++) {
        let s = 0;
        for (let k = 0; k < m; k++) if (n - k >= 0) s += h[k] * x[n - k];
        y[n] = s;
      }
      return y;
    }
    function iirNotch(x, fs, f0, r) {
      const w0 = TAU * f0 / fs;
      const b0 = 1, b1 = -2 * Math.cos(w0), b2 = 1;
      const a1 = -2 * r * Math.cos(w0), a2 = r * r;
      const y = new Array(x.length).fill(0);
      for (let n = 0; n < x.length; n++) {
        const xn = x[n];
        const xn1 = n > 0 ? x[n - 1] : 0;
        const xn2 = n > 1 ? x[n - 2] : 0;
        const yn1 = n > 0 ? y[n - 1] : 0;
        const yn2 = n > 1 ? y[n - 2] : 0;
        y[n] = (b0 * xn + b1 * xn1 + b2 * xn2 - a1 * yn1 - a2 * yn2);
      }
      return y;
    }

    function render() {
      const fs = 4000;
      const N = 240;
      const kind = $('sel-filt')?.value || 'notch';
      const x = [];
      for (let n = 0; n < N; n++) {
        const t = n / fs;
        x.push(Math.sin(TAU * 50 * t) * 0.7 + Math.sin(TAU * 400 * t) * 0.45);
      }
      let y;
      if (kind === 'ma') y = firMA(x, 9);
      else y = iirNotch(x, fs, 50, 0.95);

      const w = canvas.width, h = canvas.height;
      ctx.fillStyle = '#0b1628'; ctx.fillRect(0, 0, w, h);
      const y0 = 70, y1 = 200;
      drawGrid(ctx, w, h, y0); drawGrid(ctx, w, h, y1);
      const xs = x.map((_, i) => i / (N - 1) * w);
      plotPolyline(ctx, xs, x.map((v) => y0 - v * 40), '#38bdf8', 1.5);
      plotPolyline(ctx, xs, y.map((v) => y1 - v * 40), '#34d399', 1.5);
      ctx.fillStyle = '#9fb4cc'; ctx.font = '12px ui-sans-serif';
      ctx.fillText('输入：50 Hz 哼声 + 400 Hz 语音近似', 10, 18);
      ctx.fillText('输出', 10, 148);
      setText('filt-readout', kind === 'ma'
        ? 'FIR 滑动平均：线性相位，群延迟 ≈ (M-1)/2 个采样。50 Hz 和 400 Hz 都会被削弱，语音变闷。'
        : 'IIR 陷波：只挖 50 Hz，400 Hz 基本保留。相位非线性，可能有振铃。极点半径 r=0.95 必须在单位圆内。');
    }
    $('sel-filt')?.addEventListener('change', render);
    $('btn-play-filt')?.addEventListener('click', () => {
      const ctxA = ensureAudio();
      stopAudio();
      const fs = ctxA.sampleRate;
      const dur = 2;
      const len = Math.floor(fs * dur);
      const raw = ctxA.createBuffer(1, len, fs);
      const d = raw.getChannelData(0);
      for (let n = 0; n < len; n++) {
        const t = n / fs;
        d[n] = Math.sin(TAU * 50 * t) * 0.4 + Math.sin(TAU * 400 * t) * 0.25 + Math.sin(TAU * 800 * t) * 0.12;
      }
      const src = ctxA.createBufferSource();
      src.buffer = raw;
      const kind = $('sel-filt')?.value || 'notch';
      if (kind === 'notch') {
        const notch = ctxA.createBiquadFilter();
        notch.type = 'notch'; notch.frequency.value = 50; notch.Q.value = 16;
        src.connect(notch); notch.connect(ctxA.destination);
      } else {
        const lp = ctxA.createBiquadFilter();
        lp.type = 'lowpass'; lp.frequency.value = 180;
        src.connect(lp); lp.connect(ctxA.destination);
      }
      src.start(); currentNodes.push(src);
    });
    render();
  }
  filterLab();

  /* ───────── 选择题诊断 ───────── */
  document.querySelectorAll('.choice[data-diagnosis]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const group = btn.parentElement;
      group.querySelectorAll('.choice').forEach((b) => b.classList.remove('selected', 'correct', 'wrong'));
      const ok = btn.getAttribute('data-answer') === 'correct' || btn.getAttribute('data-correct') === 'true';
      btn.classList.add('selected', ok ? 'correct' : 'wrong');
      const fb = group.parentElement.querySelector('[data-feedback-for], .result');
      if (fb) {
        fb.classList.toggle('warn', !ok);
        fb.classList.toggle('error', !ok);
        fb.textContent = btn.getAttribute('data-diagnosis') || '';
      }
    });
  });

  /* ───────── 探究记录 ───────── */
  const INQ = 'info-u-signals-pbl-inq';
  function restoreInq() {
    try {
      const o = JSON.parse(localStorage.getItem(INQ) || '{}');
      if (o.h) $('hypothesis-input').value = o.h;
      if (o.e) $('evidence-input').value = o.e;
      if (o.c) $('conclusion-input').value = o.c;
    } catch (e) {}
  }
  restoreInq();
  $('btn-save-inq')?.addEventListener('click', () => {
    const o = {
      h: $('hypothesis-input')?.value || '',
      e: $('evidence-input')?.value || '',
      c: $('conclusion-input')?.value || ''
    };
    localStorage.setItem(INQ, JSON.stringify(o));
    setText('inq-fb', '已保存在本机。期末答辩应能把这三栏连成「问题—证据—结论」。');
  });

  document.querySelectorAll('[data-branch]').forEach((el) => {
    el.addEventListener('click', () => {
      document.querySelectorAll('[data-branch]').forEach((x) => x.classList.remove('selected-branch'));
      el.classList.add('selected-branch');
      setText('branch-fb', '已选择路径：' + (el.querySelector('h3')?.textContent || '') + '。不要跳过对应关卡答辩。');
    });
  });
})();
