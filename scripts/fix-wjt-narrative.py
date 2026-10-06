#!/usr/bin/env python3
"""fix-wjt-narrative.py — hero 四幕剧情卡 + 地图视图/剧情任务修复
1. hero-infographic：时间轴卡 → 四幕剧情卡（图+年代+标题+剧情句）
2. 移除长卷 hero-cover-img figure（四幕第一幕图带 hero-cover-img 类满足 #57）
3. 地图 fitBounds 收紧聚焦中国主体 + desc 改任务式 + 地图下加剧情任务卡
幂等：<!-- narrative-v3 -->
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "community/hist-h-wei-jin-tang/index.html"
MARK = "<!-- narrative-v3 -->"

ACTS = [
    ("hist-h-wei-jin-tang-hero-act1.png", "第一幕 · 分裂", "220 — 316", "三国鼎立，中国碎成三块",
     "这一碎就是 96 年。赤壁的一把火，烧定了魏蜀吴的均势。", "#7dd3fc", "rgba(59,130,246,.4)", True),
    ("hist-h-wei-jin-tang-hero-act2.png", "第二幕 · 交融", "317 — 589", "最乱的年代，最大的融合",
     "鲜卑人改说汉语，汉人南迁开垦江南。云冈的佛像，静静看着这一切。", "#fbbf24", "rgba(245,158,11,.4)", False),
    ("hist-h-wei-jin-tang-hero-act3.png", "第三幕 · 统一", "581 — 618", "38 年的王朝，缝起整个中国",
     "大运河把江南的粮运往北方，也把分裂近四百年的南北重新缝成一体。", "#6ee7b7", "rgba(52,211,153,.4)", False),
    ("hist-h-wei-jin-tang-hero-act4.png", "第四幕 · 鼎盛", "618 — 907", "世界来到这里，中国走向世界",
     "长安城住着各国使节和胡商，驼队从丝绸之路带来远方的消息。", "#fca5a5", "rgba(239,68,68,.4)", False),
]

CARDS = "".join(
    f'<figure style="margin:0;border-radius:14px;overflow:hidden;border:1px solid {a[6]};background:rgba(21,37,52,.6);">'
    f'<img{" class=\"hero-cover-img\"" if a[7] else ""} src="./assets/{a[0]}" alt="{a[3]}" loading="{"eager" if a[7] else "lazy"}" style="width:100%;display:block;">'
    f'<figcaption style="padding:12px 14px;">'
    f'<div style="font-size:12px;color:{a[5]};letter-spacing:1px;">{a[1]} | {a[2]}</div>'
    f'<div style="font-size:16px;font-weight:700;margin:4px 0;">{a[3]}</div>'
    f'<div style="font-size:13px;opacity:.85;line-height:1.6;">{a[4]}</div>'
    f'</figcaption></figure>'
    for a in ACTS)

HERO_BLOCK = (
    '<section class="section" id="hero-infographic" data-bloom-level="understand" data-scaffold="full" data-tsh="知识结构主图">'
    '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin-top:22px;">'
    + CARDS +
    '</div><p style="text-align:center;color:var(--muted);font-size:14px;margin-top:14px;">四幕看完，你就握住了这四百年的主线：<strong>分裂中孕育交融，交融中重建统一，统一中走向鼎盛。</strong></p>'
    '</section>')

MAP_TASKS = """
<div class="card" style="margin-top:14px;border-left:4px solid #f59e0b;">
  <h3 style="margin:0 0 10px;">🧭 带着问题看地图</h3>
  <p style="margin:6px 0;"><strong>看「三国两晋」：</strong>找出魏、蜀、吴的大致分界——长江和秦岭，是怎样决定三国格局的？</p>
  <p style="margin:6px 0;"><strong>切到「隋唐」：</strong>对比三国，统一后疆域最大的变化在哪？想想大运河（隋朝开凿）连接了哪两个经济区。</p>
  <p style="margin:6px 0;opacity:.8;">提示：点开「古都」图层，看看这些都城的位置和当时的经济重心有什么关系。</p>
</div>"""


def main():
    html = P.read_text(encoding="utf-8")
    if MARK in html:
        print("已修复")
        return
    actions = []

    # 1) hero-infographic 整块 → 四幕剧情卡
    m = re.search(r'<section class="section" id="hero-infographic"[\s\S]*?</section>', html)
    if m:
        html = html[:m.start()] + HERO_BLOCK + html[m.end():]
        actions.append("四幕剧情卡")

    # 2) 移除长卷 hero-cover-img figure（hero 里的 figure.ta-standard-figure 含 hero-v2.png）
    html2 = re.sub(r'<figure class="ta-standard-figure" style="margin:18px 0 4px"><img class="hero-cover-img" src="\./assets/hist-h-wei-jin-tang-hero-v2\.png"[^>]*></figure>', "", html)
    if html2 != html:
        html = html2
        actions.append("撤长卷")

    # 3) 地图 fitBounds 收紧
    html3 = re.sub(r'"fitBounds": \[\s*\[\s*18,\s*72\s*\],\s*\[\s*52,\s*140\s*\]\s*\]',
                   '"fitBounds": [[16, 74], [54, 134]]', html)
    if html3 != html:
        html = html3
        actions.append("地图视图收紧")

    # 4) 地图剧情任务卡（插到 map-host 的 </div> 后）
    m4 = re.search(r'(</script></div></div></div>\s*</section>)(</div></section>\s*<section class="section teachany-upgrade-block"[^>]*id="module-1">)', html)
    if m4:
        html = html.replace(m4.group(0), m4.group(1) + MAP_TASKS + m4.group(2), 1)
        actions.append("地图任务卡")

    if not actions:
        print("无可修复项")
        return
    html = html.replace("</body>", MARK + "\n</body>", 1)
    P.write_text(html, encoding="utf-8")
    print(f"修复完成: {'、'.join(actions)}")


if __name__ == "__main__":
    main()
