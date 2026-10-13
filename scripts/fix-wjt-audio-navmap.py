#!/usr/bin/env python3
"""fix-wjt-audio-navmap.py — wei-jin-tang 达标补丁
1. 注入 __NAV_NODES__ + navMapCanvas 绘制/点击/布局切换脚本（bio-h 标准模板）
2. 注入 audio-config playlist（tts s01-s10）+ teachany-audio-player.js 引用
幂等：<!-- audio-navmap-fixed -->
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "community/hist-h-wei-jin-tang/index.html"
MARK = "<!-- audio-navmap-fixed -->"

NODES = [
    {"icon": "🎯", "label": "学习目标", "target": "objectives", "color": "#3b82f6"},
    {"icon": "📝", "label": "前测", "target": "pretest", "color": "#22c55e"},
    {"icon": "📖", "label": "核心精讲", "target": "lesson-focus", "color": "#f59e0b"},
    {"icon": "🔍", "label": "深层理解", "target": "deep-understanding", "color": "#8b5cf6"},
    {"icon": "✅", "label": "后测", "target": "posttest", "color": "#ef4444"},
    {"icon": "🧭", "label": "带问题学", "target": "anchor", "color": "#06b6d4"},
    {"icon": "⚠️", "label": "易错诊所", "target": "error-clinic", "color": "#ec4899"},
    {"icon": "🧠", "label": "记忆锚点", "target": "memory-anchor", "color": "#84cc16"},
    {"icon": "🗺️", "label": "知识图谱", "target": "knowledge-graph", "color": "#14b8a6"},
]

NAVMAP_JS = """
<script>window.__NAV_NODES__ = __NODES_JSON__;</script>
<script>
(function(){
  var cv = document.getElementById('navMapCanvas');
  if (!cv) return;
  var ctx = cv.getContext('2d');
  var nodes = window.__NAV_NODES__ || [];
  var layout = 'ring', hotspots = [];
  function compute(){
    var W = cv.width, H = cv.height, n = nodes.length, i, pts = [];
    if (layout === 'ring') {
      var cx = W/2, cy = H/2, r = Math.min(W, H)/2 - 70;
      for (i = 0; i < n; i++) {
        var a = -Math.PI/2 + i * 2*Math.PI/n;
        pts.push([cx + r*Math.cos(a), cy + r*Math.sin(a)]);
      }
    } else {
      var cols = n > 6 ? 2 : 1, per = Math.ceil(n/cols);
      for (i = 0; i < n; i++) {
        var c = Math.floor(i/per), row = i%per;
        pts.push([W*(c?0.72:0.28), 60 + row*(H-100)/Math.max(1,per-1)]);
      }
    }
    return pts;
  }
  function draw(){
    var W = cv.width, H = cv.height;
    ctx.clearRect(0,0,W,H);
    var pts = compute();
    hotspots = [];
    ctx.strokeStyle = 'rgba(96,165,250,.45)'; ctx.lineWidth = 2;
    for (var i = 1; i < pts.length; i++) {
      ctx.beginPath(); ctx.moveTo(pts[i-1][0], pts[i-1][1]); ctx.lineTo(pts[i][0], pts[i][1]); ctx.stroke();
    }
    for (i = 0; i < pts.length; i++) {
      var x = pts[i][0], y = pts[i][1], nd = nodes[i];
      ctx.beginPath(); ctx.arc(x, y, 30, 0, Math.PI*2);
      ctx.fillStyle = nd.color; ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.6)'; ctx.lineWidth = 2; ctx.stroke();
      ctx.fillStyle = '#fff'; ctx.font = 'bold 13px "PingFang SC",sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(nd.icon, x, y - 2);
      ctx.font = '12px "PingFang SC",sans-serif';
      ctx.fillText(nd.label.length > 6 ? nd.label.slice(0,6) : nd.label, x, y + 14);
      hotspots.push({x:x, y:y, r:34, target:nd.target});
    }
  }
  cv.addEventListener('click', function(e){
    var rect = cv.getBoundingClientRect();
    var mx = (e.clientX - rect.left) * (cv.width / rect.width);
    var my = (e.clientY - rect.top) * (cv.height / rect.height);
    for (var i = 0; i < hotspots.length; i++) {
      var h = hotspots[i];
      if ((mx-h.x)*(mx-h.x) + (my-h.y)*(my-h.y) <= h.r*h.r) {
        var el = document.getElementById(h.target);
        if (el) el.scrollIntoView({behavior:'smooth', block:'start'});
        return;
      }
    }
  });
  var ring = document.getElementById('navLayoutRing');
  var list = document.getElementById('navLayoutList');
  if (ring) ring.addEventListener('click', function(){ layout = 'ring'; draw(); });
  if (list) list.addEventListener('click', function(){ layout = 'list'; draw(); });
  draw();
})();
</script>
"""

PLAYLIST = [
    ("s01", "开场导览", "tts/s01-hero.mp3"),
    ("s02", "问题锚点", "tts/s02-problem-anchor.mp3"),
    ("s03", "学习目标", "tts/s03-objectives.mp3"),
    ("s04", "前测说明", "tts/s04-pretest.mp3"),
    ("s05", "核心概念", "tts/s05-concept-core.mp3"),
    ("s06", "方法应用", "tts/s06-example-apply.mp3"),
    ("s07", "互动任务", "tts/s07-drag-activity.mp3"),
    ("s08", "分层练习", "tts/s08-practice.mp3"),
    ("s09", "后测说明", "tts/s09-posttest.mp3"),
    ("s10", "总结迁移", "tts/s10-summary.mp3"),
]


def main():
    html = P.read_text(encoding="utf-8")
    if MARK in html:
        print("已补丁")
        return
    actions = []

    # 1) navMap 脚本（course-nav-map section 后插入）
    if "__NAV_NODES__" not in html:
        m = re.search(r'(<section[^>]*id="course-nav-map"[\s\S]*?</section>)', html)
        if m:
            js = NAVMAP_JS.replace("__NODES_JSON__", json.dumps(NODES, ensure_ascii=False))
            html = html[:m.end(1)] + "\n" + js + html[m.end(1):]
            actions.append("navMap闭环")

    # 2) audio playlist + player.js
    if "data-teachany-audio-playlist" not in html:
        items = []
        for sid, title, src in PLAYLIST:
            items.append({"id": sid, "title": title, "src": src, "text": f"三国两晋南北朝与隋唐 · {title}导览。"})
        pl = ('<div id="audio-config" data-teachany-audio hidden>'
              '<script type="application/json" data-teachany-audio-playlist>'
              + json.dumps(items, ensure_ascii=False, indent=1) + "</script></div>")
        # 插在 hero 后（第一个 </section> 后）
        m2 = re.search(r"</section>", html)
        html = html[:m2.end()] + "\n" + pl + html[m2.end():]
        if "teachany-audio-player.js" not in html:
            html = html.replace("</body>",
                '<script src="../../assets/scripts/teachany-audio-player.js" defer></script>\n</body>', 1)
        actions.append("音频播放器")

    if not actions:
        print("无需补丁")
        return
    html = html.replace("</body>", MARK + "\n</body>", 1)
    P.write_text(html, encoding="utf-8")
    print(f"补丁完成: {'、'.join(actions)}")


if __name__ == "__main__":
    main()
