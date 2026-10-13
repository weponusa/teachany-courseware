#!/usr/bin/env python3
"""fix-wjt-map-story.py — 地图剧情化改造
1. 时代按钮 → 剧情章节（第一幕·破碎的百年 / 第二幕·重圆与鼎盛）
2. desc → 剧情脚本（带着问题看疆域，HTML）
3. cities 空数组 → 9 个剧情锚点（魏蜀吴都+赤壁/长安洛阳涿郡余杭扬州）
4. 引导文案剧情化
幂等：<!-- map-story-v1 -->
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "community/hist-h-wei-jin-tang/index.html"
MARK = "<!-- map-story-v1 -->"

ERAS_NEW = '''"eras": [
    {
      "id": "era",
      "label": "第一幕 · 破碎的百年",
      "file": "chrono-cn/005-three-kingdoms.geojson",
      "fill": "#ef4444",
      "stroke": "#ef4444",
      "desc": "<strong>中国碎成了三块。</strong>找到长江了吗？蜀、吴就躲在它和秦岭身后。280年西晋短暂缝合，可37年后又碎成十六国——这一乱，又是270年。",
      "cities": [
        [34.62, 112.45, "洛阳", "Luoyang", "魏都：220年曹丕在这里代汉建魏"],
        [30.57, 104.07, "成都", "Chengdu", "蜀都：刘备借秦岭蜀道守住一隅"],
        [32.06, 118.80, "建业", "Jianye", "吴都：长江天堑就是孙吴的城墙"],
        [29.87, 113.90, "赤壁", "Chibi", "208年，一把火烧出三国均势"]
      ]
    },
    {
      "id": "era",
      "label": "第二幕 · 重圆与鼎盛",
      "file": "chrono-cn/010-tang-dynasty.geojson",
      "fill": "#10b981",
      "stroke": "#10b981",
      "desc": "<strong>碎片重新拼成一个中国。</strong>看疆域向西伸到了哪？——西域。再看长安：它偏居西北，粮食却要从东南运来。这就是隋炀帝非挖大运河不可的原因。",
      "cities": [
        [34.27, 108.95, "长安", "Chang'an", "唐都：当时世界最大城市，万国来朝"],
        [34.62, 112.45, "洛阳", "Luoyang", "东都：大运河的中心点"],
        [39.90, 116.40, "涿郡", "Zhuojun", "运河北端：江南粮船能开到这里"],
        [30.27, 120.16, "余杭", "Yuhang", "运河南端：江南财富的起点"],
        [32.39, 119.42, "扬州", "Yangzhou", "运河与长江交汇：唐代第一商业城市"]
      ]
    }
  ]'''


def main():
    html = P.read_text(encoding="utf-8")
    if MARK in html:
        print("已修复")
        return
    actions = []

    # 1) 替换 eras 数组（从 "eras": [ 到匹配的 ]，在 "center" 前）
    m = re.search(r'"eras": \[[\s\S]*?\]\s*(?=,\s*"center")', html)
    if m:
        html = html[:m.start()] + ERAS_NEW + html[m.end():]
        actions.append("剧情章节+锚点")

    # 2) 引导文案剧情化
    html2 = html.replace(
        "点击时代/图层按钮切换地图；悬停边界，点击城市标记查看说明。",
        "两幕剧情：先看中国如何碎裂，再看它如何重圆。点开城市标记，每个地点都藏着一段故事。")
    if html2 != html:
        html = html2
        actions.append("引导文案")

    if not actions:
        print("无可修复项")
        return
    html = html.replace("</body>", MARK + "\n</body>", 1)
    P.write_text(html, encoding="utf-8")
    print(f"修复完成: {'、'.join(actions)}")


if __name__ == "__main__":
    main()
