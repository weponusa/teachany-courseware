/* TeachAny 电导率测定原理 - 交互脚本 */

/* ===== TeachAny 标准配置 ===== */
window.__TEACHANY_LEARNER_QUESTION__ = '';
window.__TEACHANY_TUTOR_CONFIG__ = {
  courseId: 'ext-58712846-conductivity-principle',
  courseTitle: '电导率测定原理',
  subject: 'chemistry', grade: '10', nodeId: 'ext-58712846',
  lessonType: 'experiment',
  getLearnerQuestion: () => window.__TEACHANY_LEARNER_QUESTION__ || '',
  getContext: () => {
    const s = document.querySelector('section.current-section') ||
      (location.hash ? document.querySelector(location.hash) : null);
    return (s || document.body).innerText.slice(0, 3000);
  }
};

function setTAQuestion(q) {
  window.__TEACHANY_LEARNER_QUESTION__ = q || '';
  const f = document.getElementById('af');
  if (f) { f.textContent = q ? '你的问题：' + q : '选择或输入后，本课会围绕你的问题展开。'; f.className = q ? 'rs' : 'rs wn'; }
}

document.querySelectorAll('[data-anchor-choice]').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('[data-anchor-choice]').forEach(x => x.classList.remove('sel'));
    b.classList.add('sel');
    setTAQuestion(b.getAttribute('data-anchor-choice') || b.textContent.trim());
  });
});
document.getElementById('lqi')?.addEventListener('input', e => setTAQuestion(e.target.value.trim()));

document.addEventListener('DOMContentLoaded', () => {
  const cv = document.querySelector('meta[name="course-version"]')?.content;
  const sv = document.querySelector('meta[name="teachany-version"]')?.content;
  if (cv) document.getElementById('cv').textContent = cv;
  if (sv) document.getElementById('sv').textContent = sv.replace(/^v/, '');
});

/* ===== Quiz interaction ===== */
function setupQuiz(id) {
  const sec = document.getElementById(id); if (!sec) return;
  const btns = sec.querySelectorAll('.ch');
  const fb = sec.querySelector('[data-feedback-for]');
  btns.forEach(b => b.addEventListener('click', () => {
    btns.forEach(x => { x.classList.remove('sel', 'ok', 'no'); });
    b.classList.add('sel');
    const ok = b.dataset.correct === 'true' || b.dataset.answer === 'correct';
    b.classList.add(ok ? 'ok' : 'no');
    if (fb) { fb.className = 'rs'; fb.innerHTML = (ok ? '✅ ' : '❌ ') + (b.dataset.diagnosis || ''); }
  }));
}
setupQuiz('pretest'); setupQuiz('conceptest-1'); setupQuiz('posttest');

/* ===== Scaffold checks ===== */
document.getElementById('sb1')?.addEventListener('click', () => {
  const v = parseFloat(document.getElementById('si1').value);
  const f = document.getElementById('sf1');
  if (isNaN(v)) { f.textContent = '请输入数值'; f.style.color = '#f59e0b'; return; }
  if (Math.abs(v - 116.7) < 2) { f.textContent = '✅ 正确！l/A = 116.7 m⁻¹'; f.style.color = 'var(--ok)'; }
  else { f.textContent = '提示：G=1/R=1/826，l/A=κ/G=0.1413/(1/826)'; f.style.color = '#f59e0b'; }
});
document.getElementById('sb2')?.addEventListener('click', () => {
  const v = parseFloat(document.getElementById('si2').value);
  const f = document.getElementById('sf2');
  if (isNaN(v)) { f.textContent = '请输入数值'; f.style.color = '#f59e0b'; return; }
  const exp = 1 / 2150 * 116.7;
  if (Math.abs(v - exp) < 0.002) { f.textContent = '✅ 正确！κ = ' + exp.toFixed(4) + ' S/m'; f.style.color = 'var(--ok)'; }
  else { f.textContent = '提示：G=1/2150，κ=G×116.7'; f.style.color = '#f59e0b'; }
});

/* ===== Canvas 1: 电导池模型 ===== */
(function () {
  const c = document.getElementById('cellC'); if (!c) return;
  const ctx = c.getContext('2d'), W = c.width, H = c.height;
  let animId;
  function draw() {
    const l = parseFloat(document.getElementById('sL').value);
    const A = parseFloat(document.getElementById('sA').value);
    const k = parseFloat(document.getElementById('sK').value);
    const cc = l / A, G = k * (A / l), R = 1 / G;
    document.getElementById('vL').textContent = l.toFixed(1) + ' cm';
    document.getElementById('vA').textContent = A.toFixed(1) + ' cm²';
    document.getElementById('vK').textContent = k.toFixed(1) + ' S/m';
    document.getElementById('rCC').textContent = cc.toFixed(2);
    document.getElementById('rG').textContent = G.toFixed(4);
    document.getElementById('rR').textContent = R.toFixed(2);
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#081426'; ctx.fillRect(0, 0, W, H);
    // Beaker
    const bL = 180, bR = 580, bT = 60, bB = 380;
    ctx.strokeStyle = '#4a6fa5'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(bL, bT); ctx.lineTo(bL, bB); ctx.lineTo(bR, bB); ctx.lineTo(bR, bT); ctx.stroke();
    // Solution fill
    const sa = Math.min(0.3 + k * 0.06, 0.8);
    ctx.fillStyle = 'rgba(56,189,248,' + sa.toFixed(2) + ')';
    ctx.fillRect(bL + 2, bT + 20, bR - bL - 4, bB - bT - 22);
    // Ions animation
    const n = Math.min(Math.floor(k * 5), 30);
    const t = Date.now() / 1000;
    ctx.font = '16px sans-serif';
    for (let i = 0; i < n; i++) {
      const x = bL + 30 + ((i * 137 + Math.sin(t + i) * 15) % (bR - bL - 60));
      const y = bT + 50 + ((i * 89 + Math.cos(t * 0.8 + i) * 12) % (bB - bT - 80));
      ctx.fillStyle = i % 2 ? '#93c5fd' : '#fca5a5';
      ctx.fillText(i % 2 ? '−' : '+', x, y);
    }
    // Electrodes
    const eW = Math.max(8, A * 18);
    const eL1 = (bL + bR) / 2 - l * 40;
    const eL2 = (bL + bR) / 2 + l * 40;
    ctx.fillStyle = '#fcd34d';
    ctx.fillRect(eL1 - eW / 2, bT + 30, eW, bB - bT - 50);
    ctx.fillRect(eL2 - eW / 2, bT + 30, eW, bB - bT - 50);
    // Electrode labels
    ctx.fillStyle = '#fcd34d'; ctx.font = '14px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('电极 A', eL1, bT + 18); ctx.fillText('电极 B', eL2, bT + 18);
    // Distance arrow
    ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(eL1, bB + 15); ctx.lineTo(eL2, bB + 15); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#94a3b8'; ctx.font = '13px sans-serif';
    ctx.fillText('l = ' + l.toFixed(1) + ' cm', (eL1 + eL2) / 2, bB + 30);
    // Area indicator
    ctx.fillStyle = '#94a3b8'; ctx.font = '13px sans-serif';
    ctx.fillText('A = ' + A.toFixed(1) + ' cm²', eL1, bB + 50);
    // Title
    ctx.fillStyle = '#eef6ff'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('电导池模型', W / 2, 30);
    ctx.textAlign = 'start';
    animId = requestAnimationFrame(draw);
  }
  draw();
  ['sL', 'sA', 'sK'].forEach(id => {
    document.getElementById(id)?.addEventListener('input', () => { cancelAnimationFrame(animId); draw(); });
  });
})();

/* ===== Canvas 2: 稀释曲线 ===== */
(function () {
  const c = document.getElementById('dilC'); if (!c) return;
  const ctx = c.getContext('2d'), W = c.width, H = c.height;
  const LmInf = 0.0126, Ks = 0.000193, Ka = 1.8e-5;
  function strongLm(c) { return LmInf - Ks * Math.sqrt(c * 1000); }
  function weakLm(c) {
    const cM3 = c * 1000;
    let alpha = (-Ka + Math.sqrt(Ka * Ka + 4 * Ka * cM3)) / (2 * cM3);
    if (alpha > 1) alpha = 1; if (alpha < 0) alpha = 0;
    return alpha * LmInf;
  }
  function draw() {
    const conc = parseFloat(document.getElementById('sC').value);
    document.getElementById('vC').textContent = conc.toFixed(3) + ' mol/L';
    const sLm = strongLm(conc), wLm = weakLm(conc);
    const alpha = conc > 0 ? (wLm / LmInf * 100) : 0;
    document.getElementById('rS').textContent = sLm.toFixed(5);
    document.getElementById('rW').textContent = wLm.toFixed(5);
    document.getElementById('rA').textContent = alpha.toFixed(1);
    ctx.clearRect(0, 0, W, H); ctx.fillStyle = '#081426'; ctx.fillRect(0, 0, W, H);
    // Plot area
    const pL = 80, pR = 720, pT = 40, pB = 360;
    ctx.strokeStyle = '#4a6fa5'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(pL, pB); ctx.lineTo(pR, pB); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(pL, pB); ctx.lineTo(pL, pT); ctx.stroke();
    // Labels
    ctx.fillStyle = '#94a3b8'; ctx.font = '13px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('浓度 √c (mol/L)½', (pL + pR) / 2, pB + 30);
    ctx.save(); ctx.translate(20, (pT + pB) / 2); ctx.rotate(-Math.PI / 2);
    ctx.fillText('Λₘ (S·m²/mol)', 0, 0); ctx.restore();
    // Y-axis ticks
    ctx.textAlign = 'right'; ctx.fillStyle = '#64748b'; ctx.font = '11px monospace';
    for (let i = 0; i <= 5; i++) {
      const y = pB - (i / 5) * (pB - pT);
      ctx.fillText((i * 2.52).toFixed(1) + '×10⁻³', pL - 4, y + 4);
      ctx.strokeStyle = 'rgba(148,163,184,.1)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(pL, y); ctx.lineTo(pR, y); ctx.stroke();
    }
    // X-axis ticks
    ctx.textAlign = 'center';
    for (let i = 1; i <= 5; i++) {
      const x = pL + (i / 5) * (pR - pL);
      ctx.fillText('0.' + (i * 2), x, pB + 16);
      ctx.strokeStyle = 'rgba(148,163,184,.1)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x, pT); ctx.lineTo(x, pB); ctx.stroke();
    }
    // Strong electrolyte curve (NaCl)
    ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 3; ctx.beginPath();
    for (let i = 1; i <= 200; i++) {
      const cVal = i * 0.005;
      const lm = strongLm(cVal);
      const x = pL + (Math.sqrt(cVal) / Math.sqrt(1)) * (pR - pL);
      const y = pB - (lm / 0.0126) * (pB - pT);
      if (i === 1) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    // Weak electrolyte curve (CH3COOH)
    ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 3; ctx.beginPath();
    for (let i = 1; i <= 200; i++) {
      const cVal = i * 0.005;
      const lm = weakLm(cVal);
      const x = pL + (Math.sqrt(cVal) / Math.sqrt(1)) * (pR - pL);
      const y = pB - (lm / 0.0126) * (pB - pT);
      if (i === 1) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    // Current point
    const sY = pB - (sLm / 0.0126) * (pB - pT);
    const wY = pB - (wLm / 0.0126) * (pB - pT);
    const cX = pL + (Math.sqrt(conc) / Math.sqrt(1)) * (pR - pL);
    // Dashed lines to points
    ctx.strokeStyle = 'rgba(56,189,248,.4)'; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(cX, pB); ctx.lineTo(cX, sY); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(pL, sY); ctx.lineTo(cX, sY); ctx.stroke(); ctx.setLineDash([]);
    ctx.strokeStyle = 'rgba(245,158,11,.4)'; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(cX, pB); ctx.lineTo(cX, wY); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(pL, wY); ctx.lineTo(cX, wY); ctx.stroke(); ctx.setLineDash([]);
    // Points
    ctx.beginPath(); ctx.arc(cX, sY, 6, 0, Math.PI * 2); ctx.fillStyle = '#38bdf8'; ctx.fill();
    ctx.beginPath(); ctx.arc(cX, wY, 6, 0, Math.PI * 2); ctx.fillStyle = '#f59e0b'; ctx.fill();
    // Legend
    ctx.fillStyle = '#38bdf8'; ctx.fillRect(pR - 180, pT + 10, 16, 4);
    ctx.fillStyle = '#94a3b8'; ctx.font = '13px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText('NaCl (强电解质)', pR - 160, pT + 16);
    ctx.fillStyle = '#f59e0b'; ctx.fillRect(pR - 180, pT + 30, 16, 4);
    ctx.fillStyle = '#94a3b8'; ctx.fillText('CH₃COOH (弱电解质)', pR - 160, pT + 36);
    // Title
    ctx.fillStyle = '#eef6ff'; ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('摩尔电导率 Λₘ vs 浓度 √c', W / 2, 20);
    ctx.textAlign = 'start';
  }
  draw();
  document.getElementById('sC')?.addEventListener('input', draw);
})();
