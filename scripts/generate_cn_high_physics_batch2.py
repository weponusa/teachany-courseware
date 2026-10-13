#!/usr/bin/env python3
"""Generate TeachAny CN high-school physics batch 2 courseware."""
from __future__ import annotations

import importlib.util
from pathlib import Path

BASE_PATH = Path(__file__).with_name("generate_cn_high_physics_batch1.py")
spec = importlib.util.spec_from_file_location("physics_batch_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(base)

BATCH_IDS = [
    "phy-h-common-forces",
    "phy-h-force-decomposition",
    "phy-h-newton-laws",
    "phy-h-projectile-motion",
    "phy-h-universal-gravitation",
]

DETAILS = {
    "phy-h-common-forces": {
        "title": "常见的力：从受力图开始看世界",
        "title_en": "Common Forces",
        "role": "受力图诊断师",
        "and": "你已经能描述物体运动，也知道运动状态改变往往来自相互作用。",
        "but": "题目里常把重力、弹力、摩擦力混在一起，如果不先画受力图，就会把不存在的力也算进去。",
        "therefore": "所以要认识重力、弹力、摩擦力和胡克定律，用接触、形变和相对运动趋势判断力。",
        "question": "怎样判断一个物体到底受了哪些力，而不是凭感觉乱加力？",
        "concepts": [("重力", "重力近似等于 mg，方向竖直向下，作用点可看作重心。"), ("弹力", "接触并发生形变时可能产生弹力，弹簧弹力满足 F=kx。"), ("摩擦力", "摩擦力阻碍相对运动或相对运动趋势，滑动摩擦力 f=μN。")],
        "facts": ["水平桌面对书的支持力来自桌面微小形变。", "静摩擦力大小不是固定 μN，而是随外力在最大静摩擦内自适应。", "弹簧伸长越大，弹力越大，前提是没有超过弹性限度。"],
        "memory": "受力先问三件事：有没有重力、有没有接触形变、有没有相对运动趋势。",
        "error": "常见错误：物体运动方向向右，就画一个“向右的运动力”。力不是运动自带的，必须来自相互作用。",
        "pretest": ("滑动摩擦力大小通常可表示为？", ["mg", "kx", "μN", "mv"], 2, "滑动摩擦力大小 f=μN。"),
        "posttest": ("弹簧在弹性限度内伸长越大，弹力通常？", ["越大", "越小", "不变", "一定为零"], 0, "胡克定律 F=kx。"),
        "interaction": "forces",
        "external": "https://phet.colorado.edu/sims/html/friction/latest/friction_zh_CN.html",
        "objectives": ["能画出常见受力图", "能区分重力、弹力和摩擦力的产生条件", "能用胡克定律和滑动摩擦公式解决基础问题"],
    },
    "phy-h-force-decomposition": {
        "title": "力的合成与分解：把一个力换成等效分量",
        "title_en": "Composition and Decomposition of Forces",
        "role": "桥梁拉索受力分析师",
        "and": "你已经能识别重力、弹力、摩擦力，也知道力有大小和方向。",
        "but": "斜面、吊桥、拉索等场景中，力不总沿坐标轴方向。直接用力的大小计算，会忽略方向贡献。",
        "therefore": "所以要用矢量平行四边形法则，把力合成或分解到方便分析的方向。",
        "question": "为什么斜向上的拉力，既能向前拉动物体，也能减小地面对物体的压力？",
        "concepts": [("矢量", "力既有大小又有方向，合成时遵循矢量运算法则。"), ("合力", "几个力共同作用的效果可用一个等效力表示。"), ("分力", "一个力可沿选定方向分解成等效分量，常用 Fx=Fcosθ、Fy=Fsinθ。")],
        "facts": ["斜面上的重力可分解为沿斜面方向和垂直斜面方向。", "共点力平衡时，合力为零。", "分解方向不是唯一的，通常按运动方向和约束方向选取。"],
        "memory": "力的分解不是把力切碎，而是换一组等效坐标语言。",
        "error": "常见错误：把分力和原来的力同时放进同一个受力图重复计算。分解后就不要再把原力也加进去。",
        "pretest": ("力是？", ["标量", "矢量", "只有大小", "没有方向"], 1, "力有大小和方向，是矢量。"),
        "posttest": ("一个力分解成两个分力后，原力和分力能否同时参与合力计算？", ["能", "不能，否则重复", "必须都写", "只看大小"], 1, "分力是原力的等效替代，不能和原力重复计入。"),
        "interaction": "decomposition",
        "external": "",
        "objectives": ["能用平行四边形法则理解合力", "能把力分解到合适方向", "能用分力分析斜面和拉力问题"],
    },
    "phy-h-newton-laws": {
        "title": "牛顿运动定律：合力如何决定加速度",
        "title_en": "Newton's Laws of Motion",
        "role": "车辆加速性能工程师",
        "and": "你已经会分析常见力，也能把力分解到运动方向。",
        "but": "物体受力不一定马上沿力的方向移动；真正直接对应的是合力和加速度，而不是速度。",
        "therefore": "所以要理解牛顿三定律，尤其用 F合=ma 连接受力分析和运动变化。",
        "question": "为什么同样的推力推空车和满载车，加速度不同？",
        "concepts": [("第一定律", "物体不受合外力时保持静止或匀速直线运动状态。"), ("第二定律", "合外力决定加速度：F合=ma，加速度方向与合力方向相同。"), ("第三定律", "作用力和反作用力大小相等、方向相反、作用在不同物体上。")],
        "facts": ["刹车时速度向前、加速度向后，因为合力向后。", "同样合力下质量越大，加速度越小。", "人推墙，墙也推人，两个力作用在不同物体上，不能抵消。"],
        "memory": "牛二核心：合力不是决定速度，而是决定速度怎样变。",
        "error": "常见错误：把作用力和反作用力画在同一个物体上相互抵消。它们作用在不同物体上。",
        "pretest": ("牛顿第二定律的表达式是？", ["F=ma", "v=at", "p=mv", "E=mc²"], 0, "牛顿第二定律：F合=ma。"),
        "posttest": ("同样合力作用下，质量越大，加速度？", ["越大", "越小", "不变", "一定为零"], 1, "a=F/m。"),
        "interaction": "newton",
        "external": "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_zh_CN.html",
        "objectives": ["能解释牛顿三定律", "能用 F合=ma 连接受力和运动", "能区分平衡力和作用反作用力"],
    },
    "phy-h-projectile-motion": {
        "title": "抛体运动：把弯曲轨迹拆成两个直线运动",
        "title_en": "Projectile Motion",
        "role": "投篮轨迹分析师",
        "and": "你已经会处理匀变速直线运动，也知道矢量可以分解。",
        "but": "抛体轨迹是曲线，看起来很复杂；如果直接沿轨迹分析，会很难写出运动关系。",
        "therefore": "所以要用运动合成与分解，把抛体运动拆成水平方向匀速和竖直方向匀变速。",
        "question": "为什么抛体运动轨迹是曲线，却可以分解成两个方向分别计算？",
        "concepts": [("独立性", "水平和竖直方向的运动可分别分析，再合成为实际轨迹。"), ("平抛运动", "初速度水平，水平匀速，竖直自由落体。"), ("斜抛运动", "初速度分解为水平和竖直分量，竖直方向受重力影响。")],
        "facts": ["平抛物体水平方向速度不变，竖直方向加速度为 g。", "同高度水平抛出时，落地时间由竖直高度决定。", "抛射角影响射程和最高点。"],
        "memory": "抛体运动口诀：水平不受力就匀速，竖直只受重力就匀变速。",
        "error": "常见错误：认为水平速度越大，竖直下落时间越长。同高度平抛的落地时间由竖直运动决定。",
        "pretest": ("平抛运动水平方向通常是？", ["匀速运动", "自由落体", "匀减速", "静止"], 0, "忽略空气阻力时，水平方向不受力，速度不变。"),
        "posttest": ("同高度平抛时，落地时间主要取决于？", ["水平初速度", "竖直高度", "物体颜色", "水平位移"], 1, "竖直方向自由落体决定落地时间。"),
        "interaction": "projectile",
        "external": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_zh_CN.html",
        "objectives": ["能把抛体运动分解为水平和竖直运动", "能分析平抛运动规律", "能解释射程、时间和高度的关系"],
    },
    "phy-h-universal-gravitation": {
        "title": "万有引力定律：从苹果到行星的同一规律",
        "title_en": "Universal Gravitation",
        "role": "卫星轨道计算师",
        "and": "你已经学习牛顿运动定律和圆周运动，知道合力可以提供向心加速度。",
        "but": "地面物体下落和月球绕地球运动看起来完全不同，牛顿的关键洞见是它们可能由同一种引力规律解释。",
        "therefore": "所以要学习万有引力定律 F=Gm₁m₂/r²，并用它解释天体运动和卫星环绕。",
        "question": "为什么距离变为 2 倍时，万有引力会变为原来的 1/4？",
        "concepts": [("引力公式", "任意两个有质量的物体之间存在引力，F=Gm₁m₂/r²。"), ("平方反比", "引力与距离平方成反比，距离增大，引力迅速减小。"), ("轨道运动", "卫星近似圆周运动时，万有引力提供向心力。")],
        "facts": ["月球绕地球运动可用万有引力提供向心力解释。", "人造卫星环绕速度来自 GMm/r²=mv²/r。", "万有引力统一了地面落体和天体运动的解释。"],
        "memory": "万有引力看两点：质量越大力越大，距离越远按平方变小。",
        "error": "常见错误：只按距离成反比而忘记平方。距离变为 2 倍，引力变为 1/4。",
        "pretest": ("万有引力与两物体距离 r 的关系是？", ["正比", "反比", "平方反比", "无关"], 2, "F=Gm₁m₂/r²。"),
        "posttest": ("卫星做圆周运动时，通常由什么提供向心力？", ["万有引力", "摩擦力", "弹力", "浮力"], 0, "卫星绕行时万有引力提供向心力。"),
        "interaction": "gravitation",
        "external": "https://phet.colorado.edu/sims/html/gravity-and-orbits/latest/gravity-and-orbits_zh_CN.html",
        "objectives": ["能写出并解释万有引力定律", "能理解平方反比关系", "能用万有引力提供向心力分析卫星运动"],
    },
}


def main():
    nodes, domains = base.read_tree_nodes()
    for node_id in BATCH_IDS:
        base.generate_course(node_id, nodes[node_id], domains[node_id], DETAILS[node_id])


if __name__ == "__main__":
    main()
