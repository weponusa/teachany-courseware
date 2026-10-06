#!/usr/bin/env python3
"""Generate all remaining TeachAny CN high-school physics courseware."""
from __future__ import annotations

import importlib.util
from pathlib import Path

BASE_PATH = Path(__file__).with_name("generate_cn_high_physics_batch1.py")
spec = importlib.util.spec_from_file_location("physics_batch_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(base)

EXCLUDE = {
    "phy-h-motion-description", "phy-h-kinematics-linear", "phy-h-uniform-acceleration", "phy-h-free-fall", "phy-h-circular-motion",
    "phy-h-common-forces", "phy-h-force-decomposition", "phy-h-newton-laws", "phy-h-projectile-motion", "phy-h-universal-gravitation",
}

SPECIAL = {
    "satellite": ("gravitation", "https://phet.colorado.edu/sims/html/gravity-and-orbits/latest/gravity-and-orbits_zh_CN.html"),
    "gravitation": ("gravitation", "https://phet.colorado.edu/sims/html/gravity-and-orbits/latest/gravity-and-orbits_zh_CN.html"),
    "work": ("energy", "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_zh_CN.html"),
    "energy": ("energy", "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_zh_CN.html"),
    "momentum": ("momentum", "https://phet.colorado.edu/sims/html/collision-lab/latest/collision-lab_zh_CN.html"),
    "collision": ("momentum", "https://phet.colorado.edu/sims/html/collision-lab/latest/collision-lab_zh_CN.html"),
    "electrostatics": ("electric", "https://phet.colorado.edu/sims/html/charges-and-fields/latest/charges-and-fields_zh_CN.html"),
    "coulomb": ("electric", "https://phet.colorado.edu/sims/html/coulombs-law/latest/coulombs-law_zh_CN.html"),
    "electric-field": ("electric", "https://phet.colorado.edu/sims/html/charges-and-fields/latest/charges-and-fields_zh_CN.html"),
    "electric-potential": ("electric", "https://phet.colorado.edu/sims/html/charges-and-fields/latest/charges-and-fields_zh_CN.html"),
    "capacitor": ("electric", ""),
    "circuits": ("circuit", "https://phet.colorado.edu/sims/html/circuit-construction-kit-dc/latest/circuit-construction-kit-dc_zh_CN.html"),
    "circuit": ("circuit", "https://phet.colorado.edu/sims/html/circuit-construction-kit-dc/latest/circuit-construction-kit-dc_zh_CN.html"),
    "electrical": ("circuit", "https://phet.colorado.edu/sims/html/ohms-law/latest/ohms-law_zh_CN.html"),
    "magnetic": ("magnetic", ""),
    "lorentz": ("magnetic", ""),
    "induction": ("magnetic", "https://phet.colorado.edu/sims/html/faradays-law/latest/faradays-law_zh_CN.html"),
    "alternating": ("magnetic", "https://phet.colorado.edu/sims/html/circuit-construction-kit-ac/latest/circuit-construction-kit-ac_zh_CN.html"),
    "electromagnetic-waves": ("wave", "https://phet.colorado.edu/sims/html/waves-intro/latest/waves-intro_zh_CN.html"),
    "vibration": ("wave", "https://phet.colorado.edu/sims/html/wave-on-a-string/latest/wave-on-a-string_zh_CN.html"),
    "wave-optics": ("wave", "https://phet.colorado.edu/sims/html/waves-intro/latest/waves-intro_zh_CN.html"),
    "gas-laws": ("gas_laws", ""),
    "photoelectric": ("modern", ""),
    "quantum": ("modern", ""),
    "atomic": ("modern", "https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_zh_CN.html"),
    "nuclear": ("modern", ""),
}

TEXTS = {
    "energy": {
        "concepts": [("功", "力和位移共同决定做功，W=Fscosθ，方向夹角不能忽略。"), ("动能/势能", "动能看速度，势能看相互作用位置，能量变化由做功连接。"), ("守恒", "只有保守力做功时机械能守恒，非保守力做功会改变机械能。")],
        "memory": "能量题先选系统，再看谁做功，最后判断是否守恒。",
        "error": "常见错误：不判断非保守力做功就直接套机械能守恒。",
    },
    "momentum": {
        "concepts": [("动量", "动量 p=mv，是描述运动状态的矢量。"), ("冲量", "冲量 I=Ft，等于动量变化量。"), ("守恒", "系统合外力冲量为零时，总动量守恒。")],
        "memory": "动量题先选系统，再看外力冲量，最后守恒或改变量。",
        "error": "常见错误：只看单个物体动量守恒，忘记守恒对象必须是系统总动量。",
    },
    "electric": {
        "concepts": [("电荷与电场", "电荷周围存在电场，电场对其他电荷有力的作用。"), ("场强/电势", "场强描述力的性质，电势描述能量性质。"), ("叠加", "多个电荷的场强按矢量叠加，方向不能忽略。")],
        "memory": "电场看力，电势看能；场强是矢量，电势是标量。",
        "error": "常见错误：把电场强度和电势混同，或把标量电势按矢量处理。",
    },
    "circuit": {
        "concepts": [("电流", "电荷定向移动形成电流，方向按正电荷移动方向规定。"), ("欧姆定律", "一段电路中 I=U/R，闭合电路还要考虑电源内阻。"), ("实验", "电学实验重在连接、读数、误差和图像处理。")],
        "memory": "电路题先判结构，再写等效电阻，最后看电源内阻和仪表影响。",
        "error": "常见错误：把电压表当导线、电流表当断路，忽略理想表的等效处理。",
    },
    "magnetic": {
        "concepts": [("磁场", "磁场对运动电荷和通电导线有力的作用。"), ("安培力/洛伦兹力", "受力大小与 B、I 或 qv 以及方向夹角有关。"), ("电磁感应", "磁通量变化可产生感应电动势，方向遵循楞次定律。")],
        "memory": "磁场题先判方向，再算大小；感应题先看磁通量怎么变。",
        "error": "常见错误：只代公式不判方向，导致安培力、洛伦兹力或感应电流方向错。",
    },
    "wave": {
        "concepts": [("振动", "周期性往复运动可用周期、频率和振幅描述。"), ("机械波", "波传播的是振动形式和能量，不是介质整体迁移。"), ("干涉/衍射", "波叠加产生加强和减弱，障碍物尺度影响衍射明显程度。")],
        "memory": "波题抓三量：v、f、λ；再看相位和叠加。",
        "error": "常见错误：把波速和质点振动速度混为一谈。",
    },
    "gas_laws": {
        "concepts": [("状态参量", "气体状态用压强、体积、温度等参量描述。"), ("实验定律", "控制一个量不变，研究另外两个量的关系。"), ("理想气体", "理想气体模型忽略分子体积和相互作用，适用于一定条件下近似分析。")],
        "memory": "气体题先看哪个量不变，再选 pV、V/T 或 p/T 关系。",
        "error": "常见错误：温度不换成热力学温度 K 就代入气体定律。",
    },
    "modern": {
        "concepts": [("量子观念", "微观能量交换常呈现不连续特征。"), ("光电效应", "是否逸出电子取决于光频率是否超过阈值。"), ("原子核", "核反应涉及质量亏损和能量释放，需守恒电荷数和质量数。")],
        "memory": "近代物理先看量子条件，再看守恒量。",
        "error": "常见错误：认为光强足够大就一定发生光电效应，忽略频率阈值。",
    },
    "gravitation": {
        "concepts": [("万有引力", "任意两有质量物体间存在引力，大小与质量乘积成正比。"), ("平方反比", "引力随距离平方增大而减小。"), ("轨道", "卫星运动常由万有引力提供向心力。")],
        "memory": "引力题抓质量、距离和向心力来源。",
        "error": "常见错误：忘记距离是平方反比，或把轨道半径和离地高度混用。",
    },
}

def choose_kind(nid: str, name: str):
    key = nid.lower()
    for token, pair in SPECIAL.items():
        if token in key:
            return pair
    if any(k in name for k in ("功", "能", "守恒")):
        return "energy", "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_zh_CN.html"
    return "energy", ""

def make_detail(node):
    nid = node["id"]
    name = node["name"]
    kind, external = choose_kind(nid, name)
    pack = TEXTS.get(kind, TEXTS["energy"])
    title = f"{name}：从真实情境到物理模型"
    question = f"怎样用物理模型解释和计算「{name}」中的关键现象？"
    return {
        "title": title,
        "title_en": name,
        "role": f"{name}问题分析师",
        "and": f"你已经掌握了前置知识，能够识别物体、相互作用、运动状态或能量变化等基本线索。",
        "but": f"一到「{name}」综合情境，题目会把文字、图像、公式和实验条件混在一起；如果不先建模，很容易套错公式。",
        "therefore": f"所以本课围绕「{name}」建立对象—条件—变量—证据的分析链，把真实情境转化为可计算、可解释的物理模型。",
        "question": question,
        "concepts": pack["concepts"],
        "facts": [
            f"「{name}」不是单独记公式，而是要先判断研究对象和适用条件。",
            f"同一现象可以用图像、公式和实验数据互相验证。",
            f"把「{name}」迁移到新情境时，最容易出错的是方向、系统边界或守恒条件。",
        ],
        "memory": pack["memory"],
        "error": pack["error"],
        "pretest": (f"分析「{name}」问题时第一步应做什么？", ["直接代公式", "先确定对象、方向和条件", "只看答案选项", "忽略单位"], 1, "先建模再计算，才能避免套错公式。"),
        "posttest": (f"如果「{name}」题目换了情境，最可靠的迁移方法是？", ["背原题答案", "重新识别对象、条件和变量关系", "只看数字大小", "忽略图像"], 1, "迁移的关键是识别同构模型，而不是背题面。"),
        "interaction": kind,
        "external": external,
        "objectives": [f"能说清{name}的核心物理量和适用条件", f"能用图像、公式或实验数据分析{name}问题", f"能把{name}模型迁移到新的真实情境"],
    }

def main():
    nodes, domains = base.read_tree_nodes()
    ids=[]
    for nid,node in nodes.items():
        if nid in EXCLUDE:
            continue
        if not (node.get('status')=='active' and node.get('courses')):
            ids.append(nid)
    print(f"remaining ids: {len(ids)}")
    for nid in ids:
        base.generate_course(nid, nodes[nid], domains[nid], make_detail(nodes[nid]))

if __name__ == "__main__":
    main()
