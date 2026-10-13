#!/usr/bin/env python3
"""Generate TeachAny CN high-school chemistry batch 2 courseware."""
from __future__ import annotations

import importlib.util
from pathlib import Path

BASE_PATH = Path(__file__).with_name("generate_cn_high_chem_batch1.py")
spec = importlib.util.spec_from_file_location("chem_batch_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(base)

BATCH_IDS = [
    "chem-h-ionic-reactions-electrolyte",
    "chem-h-ionic-equation",
    "chem-h-ion-identification",
    "chem-h-redox-equation",
    "chem-h-sodium-compounds",
]

DETAILS = {
    "chem-h-ionic-reactions-electrolyte": {
        "title": "电解质与离子反应综合：谁真的参加了反应？",
        "title_en": "Electrolytes and Ionic Reactions",
        "role": "水质检测实验员",
        "and": "你已经知道酸、碱、盐溶于水后可能导电，也见过沉淀、气体或水生成的反应现象。",
        "but": "把两个溶液混合时，烧杯里有很多离子，但并不是每个离子都真的参加反应；有些离子只是旁观者。",
        "therefore": "所以要从电解质电离出发，识别沉淀、气体、弱电解质等真正驱动力，判断离子反应能否发生。",
        "question": "两种溶液混合后，怎样判断哪些离子真的反应了，哪些只是旁观？",
        "concepts": [
            ("电解质", "在水溶液或熔融状态能导电的化合物叫电解质，酸、碱、多数盐属于常见电解质。"),
            ("离子反应条件", "溶液中离子反应通常因生成沉淀、气体、弱电解质或发生氧化还原而能持续进行。"),
            ("旁观离子", "反应前后形态和数量不变的离子没有参与净变化，是写净离子方程式时要删去的对象。"),
        ],
        "facts": ["AgNO₃ 与 NaCl 混合时，真正反应的是 Ag⁺ 和 Cl⁻。", "Na⁺、NO₃⁻ 在 AgCl 沉淀反应中只是旁观离子。", "离子反应不是“两个化学式碰撞”，而是溶液中离子重新组合并被沉淀/气体/水等带走。"],
        "memory": "离子反应四看：沉淀、气体、水，另看价态变不变。",
        "error": "常见错误：把所有可溶盐都直接写成沉淀。必须查溶解性，Na⁺、K⁺、NO₃⁻ 多数情况下仍留在溶液中。",
        "pretest": ("AgNO₃ 溶液与 NaCl 溶液混合，真正形成沉淀的离子是？", ["Na⁺ 和 NO₃⁻", "Ag⁺ 和 Cl⁻", "Ag⁺ 和 NO₃⁻", "Na⁺ 和 Cl⁻"], 1, "Ag⁺ 与 Cl⁻ 结合生成难溶的 AgCl 白色沉淀。"),
        "posttest": ("下列哪组离子在溶液中最容易发生沉淀反应？", ["Na⁺ 与 NO₃⁻", "K⁺ 与 Cl⁻", "Ba²⁺ 与 SO₄²⁻", "H⁺ 与 Na⁺"], 2, "Ba²⁺ 与 SO₄²⁻ 会生成难溶 BaSO₄。"),
        "interaction": "ion_mixer",
        "external": "",
        "objectives": ["能区分电解质、电离和自由移动离子", "能判断离子反应发生的常见条件", "能识别旁观离子与真正参加反应的离子"],
    },
    "chem-h-ionic-equation": {
        "title": "离子方程式：把化学反应写成真正发生的净变化",
        "title_en": "Net Ionic Equations",
        "role": "实验报告审核员",
        "and": "你已经会写化学方程式，也知道可溶强电解质在水中主要以离子形式存在。",
        "but": "普通化学方程式常把旁观离子也写进去，看不出反应本质；跳步写净离子式又容易漏配平和漏电荷。",
        "therefore": "所以要按“写化学方程式—拆强电解质—删旁观离子—查守恒”的流程写离子方程式。",
        "question": "怎样从完整化学方程式一步步得到正确的净离子方程式？",
        "concepts": [
            ("拆写原则", "强酸、强碱和可溶性盐写成离子；单质、氧化物、气体、沉淀、弱电解质和水通常保留化学式。"),
            ("删旁观离子", "反应前后完全相同的离子要删去，剩下的就是净离子方程式。"),
            ("双守恒检查", "净离子方程式必须同时满足原子守恒和电荷守恒，不能只看元素个数。"),
        ],
        "facts": ["AgNO₃ + NaCl = AgCl↓ + NaNO₃ 的净离子式是 Ag⁺ + Cl⁻ = AgCl↓。", "BaCl₂ 与 Na₂SO₄ 的净离子式是 Ba²⁺ + SO₄²⁻ = BaSO₄↓。", "CuSO₄ 与 NaOH 反应要写成 Cu²⁺ + 2OH⁻ = Cu(OH)₂↓，OH⁻ 前的 2 不能漏。"],
        "memory": "四步法：写、拆、删、查；最后查原子，也查电荷。",
        "error": "常见错误：把弱电解质 H₂O、沉淀 AgCl 也拆成离子，导致净离子方程式失去反应本质。",
        "pretest": ("写离子方程式时，下列哪类通常不应拆成离子？", ["可溶性钠盐", "强酸", "沉淀 AgCl", "强碱 NaOH"], 2, "沉淀、气体、水和弱电解质通常保留化学式。"),
        "posttest": ("CuSO₄ 与 NaOH 反应的净离子方程式正确的是？", ["Cu²⁺ + OH⁻ = CuOH↓", "Cu²⁺ + 2OH⁻ = Cu(OH)₂↓", "CuSO₄ + 2NaOH = Cu(OH)₂↓ + Na₂SO₄", "Na⁺ + SO₄²⁻ = Na₂SO₄"], 1, "氢氧化铜沉淀中有两个 OH⁻，且电荷守恒。"),
        "interaction": "equation",
        "external": "",
        "objectives": ["能按步骤把化学方程式改写为净离子方程式", "能判断哪些物质应拆写、哪些应保留", "能用原子守恒和电荷守恒检查结果"],
    },
    "chem-h-ion-identification": {
        "title": "离子检验与共存：用证据判断溶液里有什么",
        "title_en": "Ion Identification and Coexistence",
        "role": "未知溶液侦探",
        "and": "你已经知道某些离子相遇会生成沉淀、气体或水，也会写对应的净离子方程式。",
        "but": "真实实验里，未知溶液可能同时含多种离子；一个白色沉淀不一定只对应一种离子，检验顺序和干扰离子都会影响判断。",
        "therefore": "所以要建立“试剂—现象—离子—排除干扰”的证据链，并用反应条件判断离子能否大量共存。",
        "question": "看到一个实验现象时，怎样把它变成可靠的离子证据，而不是猜测？",
        "concepts": [
            ("特征反应", "Cl⁻ 可用 AgNO₃ 和稀 HNO₃ 检验，SO₄²⁻ 可用 Ba²⁺ 试剂并注意排除 CO₃²⁻ 干扰。"),
            ("共存判断", "若离子之间能生成沉淀、气体、弱电解质或发生氧化还原，就不能在溶液中大量共存。"),
            ("证据链", "检验不能只写现象，还要写试剂、现象、净离子方程式和排除干扰的理由。"),
        ],
        "facts": ["AgCl 和 BaSO₄ 都是白色沉淀，但对应离子和检验条件不同。", "H⁺ 与 CO₃²⁻ 不能大量共存，因为会生成 CO₂ 和 H₂O。", "Fe³⁺ 遇 OH⁻ 会生成红褐色 Fe(OH)₃ 沉淀。"],
        "memory": "检验四件套：加什么、看什么、说明什么、排除什么。",
        "error": "常见错误：看见白色沉淀就断定有 Cl⁻。SO₄²⁻、CO₃²⁻ 等也可能给出白色沉淀，必须排除干扰。",
        "pretest": ("检验 Cl⁻ 常用的试剂组合是？", ["BaCl₂ 和盐酸", "AgNO₃ 和稀 HNO₃", "NaOH 和酚酞", "石灰水"], 1, "Ag⁺ 与 Cl⁻ 生成 AgCl 白色沉淀，稀 HNO₃ 用于排除部分干扰。"),
        "posttest": ("下列离子组不能大量共存的是？", ["Na⁺、K⁺、NO₃⁻", "Ba²⁺、SO₄²⁻、Na⁺", "K⁺、Cl⁻、NO₃⁻", "Na⁺、K⁺、Cl⁻"], 1, "Ba²⁺ 与 SO₄²⁻ 生成 BaSO₄ 沉淀，不能大量共存。"),
        "interaction": "ion_mixer",
        "external": "",
        "objectives": ["能写出常见 Cl⁻、SO₄²⁻、CO₃²⁻、Fe³⁺ 的检验思路", "能用生成沉淀/气体/弱电解质判断离子共存", "能把实验现象组织成完整证据链"],
    },
    "chem-h-redox-equation": {
        "title": "氧化还原方程式配平：用电子守恒抓住反应骨架",
        "title_en": "Balancing Redox Equations",
        "role": "反应工程配平师",
        "and": "你已经理解氧化还原反应中有化合价变化，也知道氧化剂得电子、还原剂失电子。",
        "but": "复杂反应里元素多、系数多，单靠试凑容易乱；如果电子数不守恒，方程式即使元素看似配平也不可靠。",
        "therefore": "所以要用化合价升降法：标价态、列升降、求最小公倍数、配系数，再检查原子和电荷。",
        "question": "为什么氧化还原方程式配平的核心不是试凑，而是“失电子=得电子”？",
        "concepts": [
            ("化合价升降", "还原剂化合价升高，失电子；氧化剂化合价降低，得电子。升降总数必须相等。"),
            ("最小公倍数", "若一个粒子失 2e⁻，另一个得 5e⁻，就用 10 作为电子守恒总量配系数。"),
            ("守恒复查", "电子守恒确定骨架后，还要检查元素守恒、电荷守恒以及酸碱介质中的 H、O 配平。"),
        ],
        "facts": ["KMnO₄、K₂Cr₂O₇ 常作氧化剂，反应中中心元素价态降低。", "Fe²⁺ 被氧化为 Fe³⁺ 时，每个 Fe²⁺ 失去 1 个电子。", "Cl₂ 与 NaOH 反应可能发生歧化，同一元素既升价又降价。"],
        "memory": "配平口诀：标价态，找升降；求公倍，先配变价；再查全式守恒。",
        "error": "常见错误：只配元素个数，忘记电子守恒；或把氧化剂、还原剂的得失电子方向搞反。",
        "pretest": ("Fe²⁺ → Fe³⁺ 的变化属于？", ["得 1e⁻ 被还原", "失 1e⁻ 被氧化", "得 2e⁻ 被氧化", "价态不变"], 1, "Fe 从 +2 到 +3，化合价升高，失去 1 个电子，被氧化。"),
        "posttest": ("某还原剂每个粒子失 2e⁻，氧化剂每个粒子得 5e⁻，电子守恒最小总数是？", ["2", "5", "7", "10"], 3, "2 和 5 的最小公倍数是 10。"),
        "interaction": "redox",
        "external": "https://phet.colorado.edu/sims/html/balancing-chemical-equations/latest/balancing-chemical-equations_zh_CN.html",
        "objectives": ["能判断氧化剂、还原剂和电子转移方向", "能用化合价升降法配平氧化还原方程式", "能检查电子守恒、原子守恒和电荷守恒"],
    },
    "chem-h-sodium-compounds": {
        "title": "钠及其化合物：从金属钠反应看碱金属家族",
        "title_en": "Sodium and Its Compounds",
        "role": "危险化学品安全员",
        "and": "你已经知道金属能与氧气、酸或水发生反应，也见过食盐、苏打、小苏打等含钠物质。",
        "but": "金属钠不像铁那样能随手放在空气中，它遇水会剧烈反应；氧化钠、过氧化钠、碳酸钠、碳酸氢钠性质也不相同。",
        "therefore": "所以要从钠原子最外层 1 个电子出发，理解钠的强还原性和典型含钠化合物的性质差异。",
        "question": "为什么钠必须保存在煤油中，而食盐中的钠却非常稳定？",
        "concepts": [
            ("钠单质", "钠最外层只有 1 个电子，易失电子形成 Na⁺，表现出强还原性，与水反应生成 NaOH 和 H₂。"),
            ("氧化钠与过氧化钠", "Na₂O 是碱性氧化物，Na₂O₂ 可与 CO₂、H₂O 反应放出 O₂，常体现强氧化性。"),
            ("碳酸钠与碳酸氢钠", "Na₂CO₃ 俗称纯碱，碱性较强；NaHCO₃ 俗称小苏打，受热易分解并能与酸放 CO₂。"),
        ],
        "facts": ["钠与水反应的现象可概括为浮、熔、游、响、红。", "2Na + 2H₂O = 2NaOH + H₂↑，溶液遇酚酞变红。", "NaHCO₃ 受热分解可用于食品膨松，Na₂CO₃ 常用于玻璃、洗涤等工业场景。"],
        "memory": "钠单质看失电子，过氧化钠看放氧，碳酸氢钠看受热放 CO₂。",
        "error": "常见错误：把金属钠和钠离子混为一谈。Na 单质强还原，Na⁺ 已经稳定存在于食盐中，性质完全不同。",
        "pretest": ("金属钠与水反应生成的气体是？", ["氧气", "氢气", "氯气", "二氧化碳"], 1, "2Na + 2H₂O = 2NaOH + H₂↑。"),
        "posttest": ("食盐中的钠为什么不像金属钠那样遇水剧烈反应？", ["食盐里没有钠元素", "Na⁺ 已是稳定离子状态", "食盐不溶于水", "NaCl 是单质"], 1, "NaCl 中的钠以 Na⁺ 存在，已经失去电子，性质不同于金属钠。"),
        "interaction": "sodium",
        "external": "",
        "objectives": ["能解释钠单质强还原性的结构原因", "能描述钠与水反应的现象、方程式和安全要求", "能比较氧化钠、过氧化钠、碳酸钠、碳酸氢钠的典型性质"],
    },
}


def main():
    nodes, domains = base.read_tree_nodes()
    for node_id in BATCH_IDS:
        base.generate_course(node_id, nodes[node_id], domains[node_id], DETAILS[node_id])


if __name__ == "__main__":
    main()
