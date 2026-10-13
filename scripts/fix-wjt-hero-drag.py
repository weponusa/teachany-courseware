#!/usr/bin/env python3
"""fix-wjt-hero-drag.py — wei-jin-tang 格式/图/概念归类修复
1. cover subtitle 课标官话 → 教学化引入
2. hero AI插画+错位叠标 → HTML 时间轴结构图（四阶段）
3. 概念归类 4 张占位卡 → 8 张本课史实卡 + 注入拖拽判分 JS（含触屏点击兜底）
幂等：<!-- hero-drag-fixed -->
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "community/hist-h-wei-jin-tang/index.html"
MARK = "<!-- hero-drag-fixed -->"

NEW_SUBTITLE = "四百年，从三国鼎立到盛唐气象：分裂中孕育交融，交融中重建统一，统一中走向鼎盛。"

TIMELINE_HTML = """<section class="section" id="hero-infographic" data-bloom-level="understand" data-scaffold="full" data-tsh="知识结构主图">
<div style="display:flex;gap:8px;align-items:stretch;justify-content:center;flex-wrap:wrap;margin-top:24px;">
  <div style="flex:1;min-width:160px;padding:16px 14px;border-radius:14px;background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.45);">
    <div style="font-size:13px;color:#7dd3fc;letter-spacing:1px;">220 — 316</div>
    <div style="font-size:18px;font-weight:700;margin:6px 0;">三国两晋</div>
    <div style="font-size:13px;opacity:.85;line-height:1.6;">政权分立，三国鼎立<br>西晋短暂统一即乱</div>
  </div>
  <div style="align-self:center;color:#475569;font-size:18px;">→</div>
  <div style="flex:1;min-width:160px;padding:16px 14px;border-radius:14px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.45);">
    <div style="font-size:13px;color:#fbbf24;letter-spacing:1px;">317 — 589</div>
    <div style="font-size:18px;font-weight:700;margin:6px 0;">东晋十六国·南北朝</div>
    <div style="font-size:13px;opacity:.85;line-height:1.6;">民族交融，孝文帝改革<br>江南开发，承前启后</div>
  </div>
  <div style="align-self:center;color:#475569;font-size:18px;">→</div>
  <div style="flex:1;min-width:160px;padding:16px 14px;border-radius:14px;background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.45);">
    <div style="font-size:13px;color:#6ee7b7;letter-spacing:1px;">581 — 618</div>
    <div style="font-size:18px;font-weight:700;margin:6px 0;">隋</div>
    <div style="font-size:13px;opacity:.85;line-height:1.6;">重建统一，开创制度<br>三省六部·科举·大运河</div>
  </div>
  <div style="align-self:center;color:#475569;font-size:18px;">→</div>
  <div style="flex:1;min-width:160px;padding:16px 14px;border-radius:14px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.45);">
    <div style="font-size:13px;color:#fca5a5;letter-spacing:1px;">618 — 907</div>
    <div style="font-size:18px;font-weight:700;margin:6px 0;">唐</div>
    <div style="font-size:13px;opacity:.85;line-height:1.6;">繁荣开放，贞观开元<br>盛唐气象，万国来朝</div>
  </div>
</div>
</section>"""

DRAG_CHIPS = """<span class="drag-chip" draggable="true" data-zone="core">📜 孝文帝改革与民族交融</span>
        <span class="drag-chip" draggable="true" data-zone="method">🔗 用人口南迁数据分析江南开发</span>
        <span class="drag-chip" draggable="true" data-zone="apply">🏛️ 评价隋炀帝的功与过</span>
        <span class="drag-chip" draggable="true" data-zone="miscon">⚠️ 把魏晋南北朝只看作"黑暗时代"</span>
        <span class="drag-chip" draggable="true" data-zone="core">👑 三省六部与科举制</span>
        <span class="drag-chip" draggable="true" data-zone="method">🗺️ 读疆域图判断时代特征</span>
        <span class="drag-chip" draggable="true" data-zone="apply">📊 比较九品中正与科举的选官逻辑</span>
        <span class="drag-chip" draggable="true" data-zone="miscon">⚠️ 以为魏蜀吴三国同年同时建立</span>"""

DRAG_JS = """
<script>
(function(){
  var pool = document.getElementById('drag-pool');
  if (!pool) return;
  var dragged = null, sel = null;
  function checkDone(){
    var chips = document.querySelectorAll('.drag-chip');
    var placed = 0, right = 0;
    chips.forEach(function(c){
      var z = c.closest('.drop-zone');
      if (z) {
        placed++;
        if (z.dataset.accept === c.dataset.zone) { right++; c.style.borderColor = '#34d399'; }
        else { c.style.borderColor = '#f87171'; }
      }
    });
    var ro = document.getElementById('drag-readout');
    if (ro && placed === chips.length) {
      var ok = right === chips.length;
      ro.textContent = ok ? '✅ 全部归对！核心概念、方法、应用、误区分得清。'
                          : '❌ 对了 ' + right + '/' + chips.length + '，红框的再想想。';
    }
  }
  document.querySelectorAll('.drag-chip').forEach(function(chip){
    chip.addEventListener('dragstart', function(e){ dragged = chip; chip.classList.add('dragging'); });
    chip.addEventListener('dragend', function(){ chip.classList.remove('dragging'); });
    chip.addEventListener('click', function(){
      if (sel === chip) { chip.style.outline = ''; sel = null; }
      else {
        document.querySelectorAll('.drag-chip').forEach(function(c){ c.style.outline = ''; });
        chip.style.outline = '2px solid #60a5fa'; sel = chip;
      }
    });
  });
  document.querySelectorAll('.drop-zone').forEach(function(zone){
    zone.addEventListener('dragover', function(e){ e.preventDefault(); });
    zone.addEventListener('drop', function(e){
      e.preventDefault();
      if (dragged) { zone.appendChild(dragged); dragged = null; checkDone(); }
    });
    zone.addEventListener('click', function(){
      if (sel) { zone.appendChild(sel); sel.style.outline = ''; sel = null; checkDone(); }
    });
  });
})();
</script>
"""


def main():
    html = P.read_text(encoding="utf-8")
    if MARK in html:
        print("已修复")
        return
    actions = []

    # 1) cover subtitle 官话 → 教学化
    html2 = re.sub(
        r"(<h1>三国两晋南北朝与隋唐</h1><p class=\"subtitle\">)[^<]*(</p>)",
        lambda m: m.group(1) + NEW_SUBTITLE + m.group(2), html, count=1)
    if html2 != html:
        html = html2
        actions.append("subtitle")

    # 2) hero AI 图块 → 时间轴
    m = re.search(
        r'<figure class="ta-standard-figure" style="margin-top:28px"><section class="section" id="hero-infographic"[\s\S]*?</section>\s*(?:</figure>)?',
        html)
    if m:
        html = html[:m.start()] + TIMELINE_HTML + html[m.end():]
        actions.append("hero时间轴")

    # 3) 概念归类：4 占位卡 → 8 史实卡
    m2 = re.search(r'(<div class="drag-pool" id="drag-pool"[^>]*>)[\s\S]*?(</div>)', html)
    if m2 and "明确史实与时间" in m2.group(0):
        html = html[:m2.start()] + m2.group(1) + "\n        " + DRAG_CHIPS + "\n      " + m2.group(2) + html[m2.end():]
        actions.append("归类8卡")

    # 4) 拖拽 JS
    if "dragstart" not in html:
        html = html.replace("</body>", DRAG_JS + "\n</body>", 1)
        actions.append("拖拽JS")

    # 5) readout 文案更新（4 项 → 8 项）
    html = html.replace("拖完 4 项后自动判分。", "拖完全部卡片后自动判分；点卡片再点区域也可以。")

    if not actions:
        print("无可修复项")
        return
    html = html.replace("</body>", MARK + "\n</body>", 1)
    P.write_text(html, encoding="utf-8")
    print(f"修复完成: {'、'.join(actions)}")


if __name__ == "__main__":
    main()
