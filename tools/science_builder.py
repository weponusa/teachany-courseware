#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TeachAny · 小学科学课件生成器（v2 分页 · 小学视觉模式）

用途：把「小学科学课标 13 个学科核心概念中尚未建课的知识点」以统一的 v2 分页骨架
（cover → problem-anchor → objectives → pretest → 概念/互动交替 → 例题 → 概念测试 →
综合任务 → 后测 → 小结 → 知识图谱 → AI 学伴）生成为可发布的 community/<course-id> 课件。

设计约束（对齐 teachany skill）：
  · 学段视觉：body.teachany-elementary + 暖白底 + 珊瑚红/薄荷绿（visual-stage-modes.md）
  · 五件套与音频播放器：./assets/scripts/*（finalize-courseware.py 会复制到位，保证自包含）
  · 每个 data-tts 段落带 data-tts-script（定稿器据此生成真实分段 mp3）
  · 知识图谱 data-teachany-kg / AI 学伴 __TEACHANY_TUTOR_CONFIG__ / 连续音频 data-teachany-audio-playlist
  · 引用图片一律为本课 assets/ 内真实文件，禁止占位图与 /assets/ 绝对路径

用法：
  python3 tools/science_builder.py --spec sci-e-buoyancy          # 生成单课
  python3 tools/science_builder.py --all                          # 生成全部已注册 spec
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMMUNITY = REPO / "community"
TEACHANY_VERSION = "7.22.0"

# ─────────────────────────── 小学视觉模式 CSS ───────────────────────────
CSS = r"""
:root {
  --bg: #fffbf0;
  --bg-subtle: #fff7e6;
  --panel: #fffdf8;
  --card: #ffffff;
  --card-elevated: #ffffff;
  --line: #f2e3c9;
  --line-subtle: rgba(191, 155, 96, 0.16);
  --text: #3a3126;
  --text-secondary: #5c5142;
  --muted: #94866c;
  --brand: #ff6b6b;
  --brand-soft: rgba(255, 107, 107, 0.10);
  --brand-2: #4ecdc4;
  --brand-2-soft: rgba(78, 205, 196, 0.10);
  --accent: #4ecdc4;
  --accent-soft: rgba(78, 205, 196, 0.12);
  --warm: #ffd166;
  --warm-soft: rgba(255, 209, 102, 0.18);
  --ok: #22c55e;
  --warn: #f59e0b;
  --danger: #ef4444;
  --safe-top: env(safe-area-inset-top);
  --safe-bottom: env(safe-area-inset-bottom);
  --page-padding: 24px;
  --card-radius: 20px;
  --card-radius-sm: 14px;
  --slide-height: 100vh;
  --slide-height-fallback: 100dvh;
  --toolbar-height: 56px;
  --brandbar-height: 52px;
}

* { box-sizing: border-box; }
html, body { margin: 0; max-width: 100%; overflow-x: hidden; }
body {
  padding-top: var(--safe-top);
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Source Han Sans SC", system-ui, sans-serif;
  line-height: 1.75;
  font-size: 16px;
}
a { color: #e05555; text-decoration: none; }
a:hover { text-decoration: underline; }
button, a, input, select, textarea { min-height: 44px; }
img, video, canvas, svg { max-width: 100%; height: auto; }
h1, h2, h3, h4 { margin: 0; }

.slide-container {
  scroll-snap-type: y mandatory;
  overflow-y: auto;
  height: var(--slide-height-fallback, var(--slide-height));
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}
body:not(.play-mode) .slide-container { scroll-snap-type: y proximity; }
body.play-mode .slide-container { scroll-snap-type: y mandatory; overflow: hidden; }

.slide-page {
  min-height: var(--slide-height-fallback, var(--slide-height));
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: calc(var(--page-padding) + var(--brandbar-height)) var(--page-padding) var(--page-padding);
  padding-bottom: calc(var(--page-padding) + var(--toolbar-height));
  position: relative;
  overflow: visible;
}
/* margin:auto —— 富余空间时垂直居中；内容高于一屏时 auto 退化为 0，从顶部排布，
   避免 justify-content:center 造成的顶部负溢出（长页标题被切） */
.slide-page .slide-inner { max-width: 880px; width: 100%; position: relative; z-index: 2; margin: auto; }
.slide-page .slide-inner > * { width: 100%; box-sizing: border-box; }
.card .card { padding: 18px; box-shadow: none; border: 1px solid var(--line-subtle); }

/* 页型底色 */
.slide-page[data-page-type="cover"] {
  background:
    radial-gradient(ellipse at 20% 20%, rgba(255, 107, 107, 0.12), transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(78, 205, 196, 0.14), transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(255, 209, 102, 0.10), transparent 60%);
  text-align: center;
}
.slide-page[data-page-type="cover"] h1 {
  font-size: clamp(30px, 6.4vw, 52px);
  line-height: 1.16;
  background: linear-gradient(135deg, #ff6b6b 0%, #f59e0b 55%, #4ecdc4 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 14px;
}
.slide-page[data-page-type="cover"] .subtitle {
  color: var(--text-secondary); font-size: clamp(16px, 3vw, 21px);
  max-width: 700px; margin: 0 auto; font-weight: 600;
}
.slide-page[data-page-type="objectives"] {
  background: radial-gradient(circle at 0% 100%, rgba(78, 205, 196, 0.12), transparent 42%),
              radial-gradient(circle at 100% 0%, rgba(255, 107, 107, 0.08), transparent 42%);
}
.slide-page[data-page-type="concept"] {
  background: radial-gradient(circle at 30% 20%, rgba(255, 209, 102, 0.10), transparent 36%),
              radial-gradient(circle at 70% 80%, rgba(78, 205, 196, 0.09), transparent 36%);
}
.slide-page[data-page-type="interactive"] {
  background: radial-gradient(circle at 50% 0%, rgba(78, 205, 196, 0.14), transparent 42%),
              radial-gradient(circle at 80% 100%, rgba(255, 107, 107, 0.07), transparent 36%);
}
.slide-page[data-page-type="quiz"] {
  background: radial-gradient(circle at 20% 80%, rgba(255, 209, 102, 0.16), transparent 38%),
              radial-gradient(circle at 80% 20%, rgba(255, 107, 107, 0.07), transparent 38%);
}
.slide-page[data-page-type="summary"] {
  background: radial-gradient(circle at 50% 50%, rgba(78, 205, 196, 0.13), transparent 46%),
              radial-gradient(circle at 20% 20%, rgba(255, 209, 102, 0.10), transparent 32%);
}
.slide-page[data-page-type="cover"],
.slide-page[data-page-type="objectives"],
.slide-page[data-page-type="concept"],
.slide-page[data-page-type="interactive"],
.slide-page[data-page-type="quiz"],
.slide-page[data-page-type="summary"] { background-color: var(--bg); }

/* 品牌栏 */
.teachany-brand-bar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 10px 20px;
  background: rgba(255, 251, 240, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line-subtle);
  transition: transform 0.3s ease;
}
body.play-mode .teachany-brand-bar { transform: translateY(-100%); }
.brand-logo { display: flex; align-items: center; gap: 8px; color: #3a3126; text-decoration: none; font-weight: 800; }
.brand-mark { display: inline-grid; place-items: center; width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, var(--brand), var(--brand-2)); color: #fff; font-weight: 900; font-size: 14px; }
.brand-right { display: flex; align-items: center; gap: 12px; font-size: 13px; }
.brand-link { color: var(--muted); }
.brand-link:hover { color: #e05555; text-decoration: none; }
.brand-version { color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: rgba(191,155,96,.12); padding: 4px 10px; border-radius: 999px; font-size: 12px; }

/* 卡片 */
.card {
  background: var(--card);
  border: 1px solid var(--line-subtle);
  border-radius: var(--card-radius);
  padding: 24px;
  box-shadow: 0 6px 22px rgba(191, 155, 96, 0.14), 0 1px 0 rgba(255,255,255,0.8) inset;
}
.card-accent { border-top: 4px solid var(--warm); }
.card-glow { box-shadow: 0 6px 22px rgba(191,155,96,.14), 0 0 34px rgba(78,205,196,.12); }

.section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
.section-header h2 { font-size: clamp(20px, 4vw, 26px); font-weight: 800; line-height: 1.3; color: #3a3126; }

.phase-tag {
  display: inline-flex; align-items: center; gap: 6px;
  color: #e05555; background: var(--brand-soft);
  border: 1px solid rgba(255,107,107,.24);
  border-radius: 999px; padding: 5px 12px;
  font-size: 12px; font-weight: 700; letter-spacing: .4px;
}
.phase-tag[data-variant="success"] { color: #14897f; background: var(--accent-soft); border-color: rgba(78,205,196,.28); }
.phase-tag[data-variant="purple"] { color: #b07d12; background: var(--warm-soft); border-color: rgba(255,209,102,.5); }
.phase-tag[data-variant="warn"] { color: #b45309; background: rgba(245,158,11,.12); border-color: rgba(245,158,11,.28); }

.grid { display: grid; grid-template-columns: 1fr; gap: 12px; width: 100%; }
.grid.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid > * { min-width: 0; }

.flex-row { display: flex; gap: 12px; margin-top: 14px; align-items: center; flex-wrap: wrap; }
.flex-row .choice { flex: 1; min-width: 120px; text-align: center; }

.inner-card { margin: 12px 0; padding: 16px; border-radius: var(--card-radius-sm); border: 1px solid var(--line-subtle); background: var(--bg-subtle); }
.inner-card p { margin: 0 0 6px; }
.inner-card p:last-child { margin-bottom: 0; }

.objectives { display: grid; grid-template-columns: 1fr; gap: 10px; list-style: none; padding: 0; margin: 0; }
.objectives li {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 12px 16px; border-radius: var(--card-radius-sm);
  background: var(--brand-soft); border: 1px solid var(--line-subtle);
}
.objectives li::before { content: "✦"; color: var(--brand); font-size: 14px; margin-top: 2px; flex-shrink: 0; }

.choice {
  width: 100%; text-align: left;
  border: 1px solid rgba(255,107,107,.22);
  border-radius: var(--card-radius-sm);
  background: rgba(255,255,255,.85);
  color: var(--text);
  padding: 16px 20px; cursor: pointer; font-size: 15px; line-height: 1.55;
  transition: all .18s ease;
}
.choice:hover { background: var(--brand-soft); border-color: rgba(255,107,107,.45); transform: translateX(4px); }
.choice.selected { border-color: var(--brand); background: rgba(255,107,107,.16); }
.choice.correct { border-color: var(--ok); background: rgba(34,197,94,.12); }
.choice.wrong { border-color: var(--danger); background: rgba(239,68,68,.10); }
.choice:disabled { cursor: default; opacity: .95; }

input, textarea {
  width: 100%; border-radius: 12px; border: 1px solid var(--line);
  background: #fff; color: var(--text); padding: 14px 16px; font-size: 15px;
}
input:focus, textarea:focus { outline: none; border-color: var(--brand); box-shadow: 0 0 0 3px rgba(255,107,107,.14); }

.result { padding: 16px 20px; border-radius: var(--card-radius-sm); background: rgba(34,197,94,.10); border: 1px solid rgba(34,197,94,.24); font-size: 15px; }
.result.warn { background: var(--warm-soft); border-color: rgba(255,209,102,.55); }
.result.error { background: rgba(239,68,68,.09); border-color: rgba(239,68,68,.24); }

.canvas-wrap { overflow: auto; background: #fff; border: 1px solid var(--line-subtle); border-radius: 16px; padding: 16px; }

.ta-standard-figure { margin: 20px auto; max-width: 980px; }
.ta-standard-figure img { display: block; width: 100%; border-radius: 16px; border: 1px solid var(--line-subtle); background: #fff; }
.ta-standard-figure figcaption { margin-top: 10px; color: var(--muted); font-size: 14px; text-align: center; }

/* 进度条 / 底部工具栏 / 侧边导航 / FAB */
.slide-progress-bar { position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); z-index: 200; transition: width .3s ease; }
.slide-toolbar {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 100;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 10px 20px; padding-bottom: calc(10px + var(--safe-bottom));
  background: rgba(255,251,240,.95); backdrop-filter: blur(12px);
  border-top: 1px solid var(--line-subtle);
  transform: translateY(100%); transition: transform .3s ease;
}
body.play-mode .slide-toolbar, body.toolbar-visible .slide-toolbar { transform: translateY(0); }
.toolbar-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 40px; height: 40px; border: none; border-radius: 10px;
  background: rgba(191,155,96,.14); color: #5c5142; cursor: pointer; font-size: 18px;
}
.toolbar-btn:hover { background: rgba(191,155,96,.24); }
.toolbar-btn.active { background: var(--brand-soft); color: var(--brand); }
.toolbar-btn svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.toolbar-page-info { color: var(--muted); font-size: 13px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; min-width: 60px; text-align: center; }
.toolbar-progress { flex: 1; max-width: 200px; height: 4px; background: rgba(191,155,96,.2); border-radius: 2px; overflow: hidden; cursor: pointer; }
.toolbar-progress-fill { height: 100%; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .3s ease; }

.slide-sidenav {
  position: fixed; right: 12px; top: 50%; transform: translateY(-50%); z-index: 90;
  display: flex; flex-direction: column; align-items: flex-end; gap: 3px;
  opacity: 0; transition: opacity .3s ease; max-height: 70vh; overflow-y: auto;
  scrollbar-width: none; padding: 8px 4px; border-radius: 12px;
  background: rgba(255,251,240,.72); backdrop-filter: blur(12px);
  border: 1px solid var(--line-subtle);
}
.slide-sidenav::-webkit-scrollbar { display: none; }
body.play-mode .slide-sidenav, body.toolbar-visible .slide-sidenav { opacity: 1; }
.sidenav-dot { width: 26px; height: 5px; border-radius: 3px; background: rgba(191,155,96,.35); border: none; cursor: pointer; transition: all .3s cubic-bezier(.4,0,.2,1); padding: 0; flex-shrink: 0; }
.sidenav-dot:hover { background: rgba(255,107,107,.5); width: 34px; }
.sidenav-dot.active { background: var(--brand); width: 34px; box-shadow: 0 0 10px rgba(255,107,107,.45); }
.sidenav-counter { font-size: 10px; color: var(--muted); text-align: center; padding: 4px 0 2px; font-variant-numeric: tabular-nums; width: 100%; }

.play-mode-fab {
  position: fixed; bottom: 24px; right: 24px; z-index: 90; width: 48px; height: 48px;
  border-radius: 50%; border: none; background: linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 6px 20px rgba(255,107,107,.32); transition: all .3s ease;
}
.play-mode-fab:hover { transform: scale(1.08); }
body.play-mode .play-mode-fab { bottom: calc(var(--toolbar-height) + 16px + var(--safe-bottom)); }
.play-mode-fab svg { width: 22px; height: 22px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }

body.play-mode .slide-page { animation: slideIn .4s ease-out; }
@keyframes slideIn { from { opacity: .65; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }

/* ─── 小学科学专用组件 ─── */
.level-badge { display: inline-flex; align-items: center; gap: 6px; font-weight: 800; font-size: 13px; color: #b07d12; background: var(--warm-soft); border: 1px solid rgba(255,209,102,.6); border-radius: 999px; padding: 4px 12px; }
.kid-note { display: flex; align-items: flex-start; gap: 10px; padding: 14px 16px; border-radius: var(--card-radius-sm); background: var(--warm-soft); border: 1px dashed rgba(255,209,102,.8); font-size: 15px; }
.kid-note .emoji { font-size: 22px; line-height: 1.2; flex-shrink: 0; }

.lab-panel { background: #fff; border: 1px solid var(--line-subtle); border-radius: 18px; padding: 18px; }
.lab-stage { position: relative; height: 240px; border-radius: 14px; overflow: hidden; border: 1px solid var(--line-subtle); background: linear-gradient(180deg,#f7fbff 0%, #eaf6ff 62%, #d8ecff 62.5%, #cbe6ff 100%); }
.lab-stage .airline { position: absolute; left: 0; right: 0; top: 62%; height: 2px; background: rgba(78,205,196,.7); }
.lab-stage .bubble { position: absolute; bottom: 6px; width: 12px; height: 12px; border-radius: 50%; background: rgba(255,209,102,.9); border: 1px solid rgba(200,150,20,.5); animation: rise 2.6s linear infinite; }
@keyframes rise { 0% { transform: translateY(0) scale(.7); opacity: .9; } 100% { transform: translateY(-190px) scale(1.15); opacity: 0; } }
.lab-obj { position: absolute; left: 50%; transform: translateX(-50%); display: grid; place-items: center; border-radius: 10px; font-weight: 700; font-size: 13px; color: #fff; transition: top .8s cubic-bezier(.34,1.2,.5,1), background .4s ease; }
.lab-readout { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 14px; }
.readout-cell { flex: 1; min-width: 118px; background: var(--bg-subtle); border: 1px solid var(--line-subtle); border-radius: 12px; padding: 10px 12px; text-align: center; }
.readout-cell .k { display: block; font-size: 12px; color: var(--muted); }
.readout-cell .v { font-size: 20px; font-weight: 800; color: #e05555; font-variant-numeric: tabular-nums; }
.readout-cell .v.green { color: #14897f; }

.slider-row { display: flex; align-items: center; gap: 12px; margin-top: 12px; flex-wrap: wrap; }
.slider-row label { min-width: 96px; font-weight: 700; font-size: 14px; }
input[type="range"] { flex: 1; min-height: 32px; accent-color: var(--brand); }

.sort-bank { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; min-height: 56px; }
.sort-item {
  border: 1px solid rgba(255,107,107,.28); background: #fff; color: var(--text);
  border-radius: 12px; padding: 10px 14px; font-size: 14px; cursor: pointer; transition: all .18s;
}
.sort-item:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(191,155,96,.22); }
.sort-item.done { opacity: .45; cursor: default; transform: none; box-shadow: none; }
.sort-bins { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 14px; }
.sort-bin { border: 2px dashed rgba(191,155,96,.45); border-radius: 14px; padding: 12px; min-height: 120px; background: var(--bg-subtle); }
.sort-bin h4 { font-size: 15px; margin-bottom: 8px; color: #5c5142; }
.sort-bin .tag { display: inline-block; margin: 3px 4px 0 0; padding: 5px 10px; border-radius: 999px; font-size: 13px; background: #fff; border: 1px solid var(--line-subtle); }
.sort-bin.ok { border-color: rgba(78,205,196,.8); }
.sort-bin.no { border-color: rgba(239,68,68,.6); }

.step-grid { display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: 12px; }
.step { display: flex; gap: 10px; padding: 12px 14px; border-radius: 12px; background: var(--bg-subtle); border: 1px solid var(--line-subtle); }
.step .n { flex-shrink: 0; width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center; background: var(--brand); color: #fff; font-size: 13px; font-weight: 800; }
.step .n.green { background: var(--brand-2); }

.summary-item { display: flex; align-items: flex-start; gap: 10px; padding: 12px 16px; border-radius: var(--card-radius-sm); border: 1px solid var(--line-subtle); background: #fff; }
.summary-item .num { font-weight: 800; flex-shrink: 0; color: #e05555; }

.misconception { border-left: 5px solid var(--danger); background: rgba(239,68,68,.06); border-radius: 0 12px 12px 0; padding: 12px 16px; margin-top: 10px; }
.misconception .lab { font-weight: 800; color: #c2410c; font-size: 13px; }

@media (max-width: 768px) {
  :root { --page-padding: 16px; --card-radius: 16px; }
  .slide-page { padding: calc(16px + var(--brandbar-height)) 14px 16px; padding-bottom: calc(16px + var(--toolbar-height)); }
  .grid, .grid-2, .grid-3, .objectives, .sort-bins { grid-template-columns: 1fr !important; }
  .flex-row { flex-direction: column; }
  .flex-row .choice { min-width: 100%; }
  .card { padding: 18px; }
  .slide-sidenav { right: 6px; gap: 2px; padding: 6px 3px; }
  .sidenav-dot { width: 20px; height: 4px; }
  .teachany-brand-bar { padding: 8px 12px; }
  .brand-name { display: none; }
  .lab-stage { height: 200px; }
}
@media (max-width: 480px) {
  .slide-page[data-page-type="cover"] h1 { font-size: 26px; }
  .toolbar-progress { max-width: 110px; }
}
"""

# ─────────────────────────── 分页控制器 JS ───────────────────────────
CONTROLLER_JS = r"""
(function() {
  'use strict';
  const container = document.getElementById('slide-container');
  const pages = Array.from(document.querySelectorAll('.slide-page'));
  const totalPages = pages.length;
  let currentPage = 0, isPlayMode = false, isAutoPlay = false, autoPlayTimer = null;

  const progressBar = document.getElementById('slide-progress-bar');
  const sidenav = document.getElementById('slide-sidenav');
  const fab = document.getElementById('play-mode-fab');
  const fabIconPlay = document.getElementById('fab-icon-play');
  const fabIconBrowse = document.getElementById('fab-icon-browse');
  const tbPrev = document.getElementById('tb-prev');
  const tbNext = document.getElementById('tb-next');
  const tbPageInfo = document.getElementById('tb-page-info');
  const tbProgressFill = document.getElementById('tb-progress-fill');
  const tbProgress = document.getElementById('tb-progress');
  const tbAutoplay = document.getElementById('tb-autoplay');
  const tbFullscreen = document.getElementById('tb-fullscreen');

  function buildSidenav() {
    sidenav.innerHTML = '';
    const counter = document.createElement('div');
    counter.className = 'sidenav-counter';
    counter.id = 'sidenav-counter';
    counter.textContent = '1/' + totalPages;
    sidenav.appendChild(counter);
    pages.forEach((page, i) => {
      const dot = document.createElement('button');
      dot.className = 'sidenav-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('data-tooltip', (page.dataset.tsh || '').split(' - ')[0] || ('第' + (i + 1) + '页'));
      dot.setAttribute('aria-label', '跳转到第' + (i + 1) + '页');
      dot.addEventListener('click', () => goToPage(i));
      sidenav.appendChild(dot);
    });
  }

  function updateUI() {
    const progress = totalPages > 1 ? (currentPage / (totalPages - 1)) * 100 : 100;
    progressBar.style.width = progress + '%';
    tbProgressFill.style.width = progress + '%';
    tbPageInfo.textContent = (currentPage + 1) + ' / ' + totalPages;
    sidenav.querySelectorAll('.sidenav-dot').forEach((dot, i) => dot.classList.toggle('active', i === currentPage));
    const counterEl = document.getElementById('sidenav-counter');
    if (counterEl) counterEl.textContent = (currentPage + 1) + '/' + totalPages;
    tbPrev.style.opacity = currentPage === 0 ? '0.3' : '1';
    tbNext.style.opacity = currentPage === totalPages - 1 ? '0.3' : '1';
  }

  function goToPage(index) {
    if (index < 0 || index >= totalPages) return;
    currentPage = index;
    if (isPlayMode) pages[currentPage].scrollIntoView({ behavior: 'smooth', block: 'start' });
    else container.scrollTo({ top: pages[currentPage].offsetTop, behavior: 'smooth' });
    updateUI();
    dispatchPageAudio();
  }
  function nextPage() { if (currentPage < totalPages - 1) goToPage(currentPage + 1); }
  function prevPage() { if (currentPage > 0) goToPage(currentPage - 1); }

  let scrollTimeout;
  container.addEventListener('scroll', () => {
    if (isPlayMode) return;
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      const scrollTop = container.scrollTop;
      let closest = 0, minDist = Infinity;
      pages.forEach((page, i) => {
        const dist = Math.abs(page.offsetTop - scrollTop);
        if (dist < minDist) { minDist = dist; closest = i; }
      });
      if (closest !== currentPage) { currentPage = closest; updateUI(); }
    }, 100);
  }, { passive: true });

  function togglePlayMode() {
    isPlayMode = !isPlayMode;
    document.body.classList.toggle('play-mode', isPlayMode);
    document.body.classList.toggle('toolbar-visible', isPlayMode);
    fabIconPlay.style.display = isPlayMode ? 'none' : 'block';
    fabIconBrowse.style.display = isPlayMode ? 'block' : 'none';
    if (isPlayMode) goToPage(currentPage);
  }
  fab.addEventListener('click', togglePlayMode);
  tbPrev.addEventListener('click', prevPage);
  tbNext.addEventListener('click', nextPage);
  tbProgress.addEventListener('click', (e) => {
    const rect = tbProgress.getBoundingClientRect();
    goToPage(Math.round(((e.clientX - rect.left) / rect.width) * (totalPages - 1)));
  });
  tbAutoplay.addEventListener('click', () => {
    isAutoPlay = !isAutoPlay;
    tbAutoplay.classList.toggle('active', isAutoPlay);
    if (isAutoPlay) {
      stopAutoPlay();
      autoPlayTimer = setInterval(() => {
        if (currentPage < totalPages - 1) nextPage();
        else { stopAutoPlay(); isAutoPlay = false; tbAutoplay.classList.remove('active'); }
      }, 9000);
    } else stopAutoPlay();
  });
  function stopAutoPlay() { if (autoPlayTimer) { clearInterval(autoPlayTimer); autoPlayTimer = null; } }
  tbFullscreen.addEventListener('click', () => {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  });

  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case ' ': e.preventDefault(); nextPage(); break;
      case 'ArrowLeft': case 'ArrowUp': e.preventDefault(); prevPage(); break;
      case 'f': case 'F': if (!e.ctrlKey && !e.metaKey) togglePlayMode(); break;
      case 'Escape': if (isPlayMode) togglePlayMode(); break;
    }
  });

  function dispatchPageAudio() {
    const page = pages[currentPage];
    const ttsId = page.dataset.tts;
    if (ttsId && window.__TEACHANY_AUDIO_PLAYER__) window.__TEACHANY_AUDIO_PLAYER__.playSection(ttsId);
  }
  document.addEventListener('teachany-audio-ended', () => {
    if (isAutoPlay && currentPage < totalPages - 1) setTimeout(nextPage, 1000);
  });

  window.__TEACHANY_LEARNER_QUESTION__ = '';
  window.__TEACHANY_TUTOR_CONFIG__ = {
    courseId: '__COURSE_ID__',
    courseTitle: '__TITLE__',
    subject: 'science',
    grade: '__GRADE__',
    nodeId: '__NODE_ID__',
    lessonType: '__LESSON_TYPE__',
    getLearnerQuestion: () => window.__TEACHANY_LEARNER_QUESTION__ || '',
    getContext: () => ((pages[currentPage] || document.body).innerText || '').slice(0, 3000)
  };

  function setLearnerQuestion(q) {
    window.__TEACHANY_LEARNER_QUESTION__ = q || '';
    const fb = document.getElementById('anchor-feedback');
    if (fb) fb.textContent = q ? '你的问题：' + q : '选择或输入后，这节课会围绕你的问题展开。';
  }
  document.querySelectorAll('[data-anchor-choice]').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-anchor-choice]').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      setLearnerQuestion(btn.getAttribute('data-anchor-choice') || btn.textContent.trim());
    });
  });
  document.getElementById('learner-question-input')?.addEventListener('input', (e) => setLearnerQuestion(e.target.value.trim()));

  buildSidenav();
  updateUI();
  document.body.classList.add('toolbar-visible');
  setTimeout(() => { if (!isPlayMode) document.body.classList.remove('toolbar-visible'); }, 3000);

  document.addEventListener('DOMContentLoaded', () => {
    const cv = document.querySelector('meta[name="course-version"]')?.content;
    const sv = document.querySelector('meta[name="teachany-version"]')?.content;
    if (cv) document.getElementById('course-version-display').textContent = cv;
    if (sv) document.getElementById('skill-version-display').textContent = sv.replace(/^v/, '');
  });

  if (location.hostname === 'localhost' || location.search.includes('debug')) {
    const checks = [
      ['slide-pages', () => pages.length >= 8],
      ['course-id meta', () => !!document.querySelector('meta[name="course-id"]')?.content],
      ['template-version meta', () => document.querySelector('meta[name="teachany-template-version"]')?.content === '2.0'],
      ['side-navigation', () => sidenav.children.length > 0],
      ['audio playlist', () => !!document.querySelector('[data-teachany-audio-playlist]')],
      ['AI tutor card', () => !!document.querySelector('[data-teachany-tutor-card]')],
      ['knowledge graph', () => !!document.querySelector('[data-teachany-kg]')]
    ];
    checks.forEach(([name, fn]) => console[fn() ? 'log' : 'warn']('[TeachAny v2] ' + (fn() ? 'PASS' : 'MISSING') + ' ' + name));
  }
})();
"""


# ─────────────────────────── 页面构件 ───────────────────────────
def p_cover(spec):
    return f'''
  <section class="slide-page" data-page-type="cover" data-page-index="0" data-tts="hero"
           data-tts-script="{spec['tts']['hero']}"
           data-tsh="开场 - 用一个真实问题建立学习动机" data-bloom-level="remember" data-scaffold="full">
    <div class="slide-inner">
      <p class="level-badge">小学{spec['grade_cn']} · {spec['domain_cn']}</p>
      <h1>{spec['title']}</h1>
      <p class="subtitle">{spec['hero_question']}</p>
      <figure class="ta-standard-figure" style="margin-top:24px">
        <img src="./assets/{spec['id']}-hero.webp" alt="{spec['hero_alt']}">
        <figcaption>{spec['hero_caption']}</figcaption>
      </figure>
    </div>
  </section>'''


def p_anchor(spec):
    choices = "\n".join(
        f'          <button class="choice" data-anchor-choice="{c["v"]}"><strong>{c["t"]}</strong><br><span style="color:var(--muted);font-size:14px">{c["d"]}</span></button>'
        for c in spec['anchor_choices']
    )
    return f'''
  <section class="slide-page" id="problem-anchor" data-page-type="interactive" data-page-index="1"
           data-tts="problem-anchor" data-tts-alias="anchor"
           data-tts-script="{spec['tts']['problem-anchor']}"
           data-tsh="问题锚点 - 先确定今天最想弄明白的问题">
    <div class="slide-inner">
      <div class="card card-accent">
        <div class="section-header">
          <span class="phase-tag">问题锚点</span>
          <h2>{spec['anchor_title']}</h2>
        </div>
        <p style="color:var(--muted);margin:0 0 16px">{spec['anchor_intro']}</p>
        <div class="grid">
{choices}
        </div>
        <label style="display:block;margin-top:20px;color:var(--muted);font-size:14px">或者，写下你自己最想知道的问题
          <input id="learner-question-input" placeholder="把你好奇的问题写在这里" style="margin-top:8px">
        </label>
        <p id="anchor-feedback" class="result warn" style="margin-top:16px">选择或输入后，这节课会围绕你的问题展开。</p>
      </div>
    </div>
  </section>'''


def p_objectives(spec):
    items = "\n".join(f'          <li>{o}</li>' for o in spec['objectives'])
    return f'''
  <section class="slide-page" data-page-type="objectives" data-page-index="2" data-tts="objectives"
           data-tts-script="{spec['tts']['objectives']}"
           data-tsh="学习目标 - 明确这节课结束时能做到什么" data-bloom-level="understand">
    <div class="slide-inner">
      <div class="card">
        <div class="section-header">
          <span class="phase-tag" data-variant="success">学习目标</span>
          <h2>这节课结束时，你应该能做到</h2>
        </div>
        <ul class="objectives">
{items}
        </ul>
        <div class="kid-note" style="margin-top:16px">
          <span class="emoji">🎯</span>
          <div><strong>课标依据：</strong>{spec['standard_ref']}</div>
        </div>
      </div>
    </div>
  </section>'''


def p_quiz(spec, pid, idx, tts, title, script, questions, tag="前测"):
    qs = []
    for i, q in enumerate(questions, 1):
        opts = "\n".join(
            f'            <button class="choice" data-q="{pid}-{i}" data-correct="{"1" if o[1] else "0"}">{o[0]}</button>'
            for o in q['options']
        )
        qs.append(f'''        <div class="inner-card" data-quiz-block="{pid}-{i}">
          <p><strong>{i}. {q["q"]}</strong></p>
          <div class="grid" style="margin-top:10px">
{opts}
          </div>
          <p class="result warn" data-explain="{pid}-{i}" style="display:none;margin-top:10px">{q["explain"]}</p>
        </div>''')
    body = "\n".join(qs)
    return f'''
  <section class="slide-page" data-page-type="quiz" data-page-index="{idx}" data-tts="{tts}"
           data-tts-script="{script}"
           data-tsh="{title} - 用选择题把想法暴露出来" data-bloom-level="apply">
    <div class="slide-inner">
      <div class="card">
        <div class="section-header">
          <span class="phase-tag" data-variant="warn">{tag}</span>
          <h2>{title}</h2>
        </div>
        <p style="color:var(--muted);margin:0 0 6px">先凭直觉选一个，选完立刻看到解释——错了也没关系，正好知道要重点听哪里。</p>
{body}
        <p id="{pid}-score" class="result" style="margin-top:14px;display:none"></p>
      </div>
    </div>
  </section>'''


def p_concept(spec, pid, idx, tts, title, script, body_html, tag, bloom="understand", scaffold="full"):
    return f'''
  <section class="slide-page" data-page-type="concept" data-page-index="{idx}" data-tts="{tts}"
           data-tts-script="{script}"
           data-tsh="{title}" data-bloom-level="{bloom}" data-scaffold="{scaffold}">
    <div class="slide-inner">
      <div class="card">
        <div class="section-header">
          <span class="phase-tag">{tag}</span>
          <h2>{title}</h2>
        </div>
{body_html}
      </div>
    </div>
  </section>'''


def p_interactive(spec, pid, idx, tts, title, script, body_html, tag="动手实验室", bloom="apply"):
    return f'''
  <section class="slide-page" data-page-type="interactive" data-page-index="{idx}" data-tts="{tts}"
           data-tts-script="{script}"
           data-tsh="{title}" data-bloom-level="{bloom}" data-scaffold="partial">
    <div class="slide-inner">
      <div class="card card-glow">
        <div class="section-header">
          <span class="phase-tag" data-variant="success">{tag}</span>
          <h2>{title}</h2>
        </div>
{body_html}
      </div>
    </div>
  </section>'''


def p_summary(spec, idx, tts, title, script, body_html, tag="小结"):
    return f'''
  <section class="slide-page" data-page-type="summary" data-page-index="{idx}" data-tts="{tts}"
           data-tts-script="{script}"
           data-tsh="{title}" data-bloom-level="understand">
    <div class="slide-inner">
      <div class="card">
        <div class="section-header">
          <span class="phase-tag" data-variant="purple">{tag}</span>
          <h2>{title}</h2>
        </div>
{body_html}
      </div>
    </div>
  </section>'''


def insight_box(lenses):
    """深层理解卡（五镜头：看见它/拆开它/解释它/比较它/迁移它 中选 2-3 个）。"""
    items = "\n".join(
        f'''          <div class="inner-card">
            <p><strong>{l['lens']}</strong>：{l['text']}</p>
          </div>''' for l in lenses
    )
    return f'''
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45);margin-top:16px">
          <p style="margin:0 0 8px"><strong>🔍 深层理解</strong>　换个角度再看一遍这件事，看看能不能说出背后的原理。</p>
          <div class="grid">
{items}
          </div>
        </div>'''


def p_homework(spec, idx, tts, title, script, levels, tag="作业分层"):
    """三段式分层作业页：⭐ 基础巩固 / ⭐⭐ 能力应用 / ⭐⭐⭐ 迁移挑战。"""
    stars = {1: "⭐ 基础巩固（必做）", 2: "⭐⭐ 能力应用（必做）", 3: "⭐⭐⭐ 迁移挑战（选做）"}
    blocks = []
    for i, lv in enumerate(levels, 1):
        tasks = "\n".join(f'            <li>{t}</li>' for t in lv)
        blocks.append(f'''        <div class="inner-card">
          <p><strong>{stars[i]}</strong></p>
          <ul class="objectives" style="margin-top:8px">
{tasks}
          </ul>
        </div>''')
    body = "\n".join(blocks)
    return f'''
  <section class="slide-page" data-page-type="quiz" data-page-index="{idx}" data-tts="{tts}"
           data-tts-script="{script}"
           data-tsh="{title}" data-bloom-level="create" data-scaffold="none">
    <div class="slide-inner">
      <div class="card">
        <div class="section-header">
          <span class="phase-tag" data-variant="warn">{tag}</span>
          <h2>{title}</h2>
        </div>
        <p style="color:var(--muted);margin:0 0 12px">三层练习，做完第一、二层就算通关；第三层留给愿意继续探索的同学。</p>
{body}
      </div>
    </div>
  </section>'''


def p_kg(spec, idx):
    return f'''
  <section class="slide-page" data-page-type="summary" data-page-index="{idx}" data-tts="knowledge-graph"
           data-tts-script="{spec['tts']['knowledge-graph']}"
           data-tsh="知识图谱 - 看看这节课在科学知识网里的位置">
    <div class="slide-inner">
      <div class="card card-glow">
        <div class="section-header">
          <span class="phase-tag" data-variant="purple">知识图谱</span>
          <h2>这节课在知识网络里的位置</h2>
        </div>
        <p style="color:var(--muted);margin:0 0 16px">左边是学它之前要先会的，右边是学会之后可以继续探索的，下面是同一领域的伙伴知识。</p>
        <div data-teachany-kg="{spec['node_id']}">
          <canvas class="tkg-fallback-canvas" width="720" height="140" aria-label="知识图谱互动画布" style="display:block;width:100%;border-radius:12px;"></canvas>
        </div>
      </div>
    </div>
  </section>'''


def p_tutor(spec, idx):
    return f'''
  <section class="slide-page" data-page-type="interactive" data-page-index="{idx}" data-tts="ai-tutor"
           data-tts-script="{spec['tts']['ai-tutor']}"
           data-tsh="AI 学伴 - 先诊断卡点，再给最小提示">
    <div class="slide-inner">
      <div data-teachany-tutor-card></div>
    </div>
  </section>'''


# ─────────────────────────── 组装 ───────────────────────────
def build_html(spec):
    pages = spec['build_pages']()
    n = len(pages)
    playlist = []
    order = []
    for m in re.finditer(r'<section\b[^>]*\bdata-tts="([^"]+)"', "\n".join(pages)):
        order.append(m.group(1))
    labels = spec['tts_labels']
    for i, sec in enumerate(order, 1):
        playlist.append({
            "id": f"s{i:02d}-{sec}",
            "section": sec,
            "src": f"./tts/s{i:02d}-{sec}.mp3",
            "label": labels.get(sec, sec),
        })

    head_meta = f'''<meta name="course-id" content="{spec['id']}">
<meta name="course-title" content="{spec['title']}">
<meta name="course-subject" content="science">
<meta name="course-grade" content="小学{spec['grade_cn']}">
<meta name="course-prereqs" content="{spec.get('prereqs_meta','')}">
<meta name="course-next" content="{spec.get('next_meta','')}">
<meta name="course-version" content="{spec['version']}">
<meta name="teachany-version" content="{TEACHANY_VERSION}">
<meta name="teachany-node" content="{spec['node_id']}">
<meta name="teachany-subject" content="science">
<meta name="teachany-grade" content="{spec['grade']}">
<meta name="teachany-stage" content="elementary">
<meta name="teachany-domain" content="{spec['domain']}">
<meta name="teachany-prerequisites" content="{spec.get('prereqs_name','')}">
<meta name="teachany-lesson-type" content="{spec['lesson_type']}">
<meta name="teachany-free-mode" content="false">
<meta name="teachany-template-version" content="2.0">'''

    html = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>《{spec['title']}》 · 小学科学 {spec['grade_cn']} · TeachAny</title>
<meta name="description" content="{spec['description']}">

{head_meta}

<link rel="stylesheet" href="../../assets/scripts/ai-tutor.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-tutor-card.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-tts-narrator.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-section-hints.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-knowledge-graph.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-audio-player.css">
<link rel="stylesheet" href="../../assets/scripts/teachany-floating-dock.css">

<style>
{CSS}
</style>
</head>
<body class="teachany-elementary">

<div class="slide-progress-bar" id="slide-progress-bar" style="width: 0%"></div>

<div class="teachany-brand-bar">
  <a class="brand-logo" href="https://www.teachany.cn/" aria-label="TeachAny">
    <span class="brand-mark">T</span><span class="brand-name">TeachAny</span>
  </a>
  <div class="brand-right">
    <a class="brand-link" href="https://www.teachany.cn/">Gallery</a>
    <span class="brand-version">v<span id="course-version-display">{spec['version']}</span> · skill v<span id="skill-version-display">{TEACHANY_VERSION}</span></span>
  </div>
</div>

<div class="slide-container" id="slide-container">
{chr(10).join(pages)}
</div><!-- .slide-container -->

<div id="audio-config" data-teachany-audio hidden>
  <script type="application/json" data-teachany-audio-playlist>
{json.dumps(playlist, ensure_ascii=False, indent=2)}
  </script>
</div>

<nav class="slide-sidenav" id="slide-sidenav" aria-label="页面导航"></nav>

<button class="play-mode-fab" id="play-mode-fab" aria-label="切换播放模式" title="切换播放模式">
  <svg id="fab-icon-play" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
  <svg id="fab-icon-browse" viewBox="0 0 24 24" style="display:none"><path d="M4 6h16M4 12h16M4 18h16"></path></svg>
</button>

<div class="slide-toolbar" id="slide-toolbar">
  <button class="toolbar-btn" id="tb-prev" aria-label="上一页" title="上一页"><svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"></polyline></svg></button>
  <div class="toolbar-progress" id="tb-progress" title="进度"><div class="toolbar-progress-fill" id="tb-progress-fill"></div></div>
  <span class="toolbar-page-info" id="tb-page-info">1 / {n}</span>
  <button class="toolbar-btn" id="tb-next" aria-label="下一页" title="下一页"><svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"></polyline></svg></button>
  <button class="toolbar-btn" id="tb-autoplay" aria-label="自动播放" title="自动播放"><svg viewBox="0 0 24 24"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path></svg></button>
  <button class="toolbar-btn" id="tb-fullscreen" aria-label="全屏" title="全屏"><svg viewBox="0 0 24 24"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg></button>
</div>

<script>
{CONTROLLER_JS.replace('__COURSE_ID__', spec['id']).replace('__TITLE__', spec['title']).replace('__GRADE__', str(spec['grade'])).replace('__NODE_ID__', spec['node_id']).replace('__LESSON_TYPE__', spec['lesson_type'])}
</script>

<script>
{spec['custom_js']}
</script>

<script src="../../assets/scripts/ai-tutor.js"></script>
<script src="../../assets/scripts/teachany-tutor-card.js" defer></script>
<script src="../../assets/scripts/teachany-tts-narrator.js" defer></script>
<script src="../../assets/scripts/teachany-section-hints.js" defer></script>
<script src="../../assets/scripts/teachany-knowledge-graph.js" defer></script>
<script src="../../assets/scripts/teachany-audio-player.js?v=paged-20260919" defer></script>
</body>
</html>
'''
    return html, n, playlist


def build_manifest(spec, slide_count, playlist):
    return {
        "id": spec['id'],
        "course_id": spec['id'],
        "node_id": spec['node_id'],
        "name": spec['title'],
        "name_en": spec['name_en'],
        "subject": "science",
        "grade": str(spec['grade']),
        "stage": "elementary",
        "domain": spec['domain'],
        "lesson_type": spec['lesson_type'],
        "status": "community",
        "author": "TeachAny",
        "version": spec['version'],
        "teachany_version": TEACHANY_VERSION,
        "template_version": "2.0",
        "slide_count": slide_count,
        "curriculum": "义务教育科学课程标准（2022年版2025年修订）· 小学",
        "description": spec['description'],
        "tags": spec['tags'],
        "prerequisites": spec.get('prereqs', []),
        "leads_to": spec.get('leads_to', []),
        "learning_objectives": spec['objectives_plain'],
        "curriculum_standards": spec['standards'],
        "assets": {
            "hero": f"assets/{spec['id']}-hero.webp",
            "tts_manifest": "tts/manifest.json",
            "images": [f"assets/{spec['id']}-hero.webp"] + spec.get('section_images', []),
        },
        "has_tts": True,
        "has_video": False,
        "has_images": True,
        "has_hero": True,
        "has_canvas": True,
        "has_knowledge_graph": True,
        "free_mode": False,
        "audio_playlist": playlist,
        "created_at": "2026-09-19",
        "updated_at": "2026-09-19",
    }


def build_plan(spec):
    n = len(spec['build_pages']())
    return f"""# {spec['title']} · 课件构建方案

**学科/学段**：小学科学 · {spec['grade_cn']}
**课型**：{spec['lesson_type']}
**知识树节点**：`{spec['node_id']}`（新增，补齐课标空缺）
**课标依据**：{spec['standard_ref']}
**总页数**：{n} 页（起：锚点/目标/前测 → 承：概念与互动交替 → 转：例题与概念测试 → 合：综合任务、后测、小结、分层作业、知识图谱、AI 学伴）

## 设计思路

{spec['plan_intro']}

## 逐页方案

| 页 | 页型 | 标题（结论句） | 认知功能 |
|---|---|---|---|
{spec['plan_table']}

## 待补充素材

{spec['plan_assets']}
"""


def emit(spec):
    cid = spec['id']
    out = COMMUNITY / cid
    (out / "assets").mkdir(parents=True, exist_ok=True)
    (out / "tts").mkdir(parents=True, exist_ok=True)

    html, slide_count, playlist = build_html(spec)
    # 清除模板占位注释（若存在）
    html = re.sub(r'<!--\s*=+\s*TeachAny v2 分页课件骨架.*?-->', '', html, flags=re.S)
    (out / "index.html").write_text(html, encoding="utf-8")
    (out / "manifest.json").write_text(
        json.dumps(build_manifest(spec, slide_count, playlist), ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "PLAN.md").write_text(build_plan(spec), encoding="utf-8")
    if spec.get("hints"):
        (out / "section-hints.json").write_text(
            json.dumps(spec["hints"], ensure_ascii=False, indent=2), encoding="utf-8")
    return out, slide_count, playlist


def load_spec(module_name):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    mod = __import__(f"science_specs.{module_name}", fromlist=["SPEC"])
    return mod.SPEC


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    names = args.spec
    if args.all or not names:
        names = sorted(p.stem for p in (Path(__file__).resolve().parent / "science_specs").glob("*.py")
                       if not p.name.startswith("_"))
    for n in names:
        spec = load_spec(n)
        out, cnt, pl = emit(spec)
        print(f"✅ {spec['id']} → {out}  ({cnt} 页, {len(pl)} 段音频槽)")


if __name__ == "__main__":
    main()
