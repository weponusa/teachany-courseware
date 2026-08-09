#!/usr/bin/env python3
"""Add topic-specific depth modules to bio-h shell courses.

These high-school biology courses pass the teaching gate via many template
sections (text-module / 五镜头), but lack topic-specific core teaching. Each
course gets two modules: 知识精讲 + 方法范例 (worked example + diagnostic +
常见误区). No mp4. Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-09"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit,
    )


COURSES = {
    "bio-h-atp": C(
        "ATP：生命活动的直接能源",
        "ATP（三磷酸腺苷）是细胞内的直接能源物质，结构可简记为 A—P～P～P，远离腺苷的两个高能磷酸键水解时释放能量。细胞中 ATP 与 ADP 迅速转化：ATP 水解供能，ADP+Pi+能量再合成 ATP。糖类、脂肪等是主要能源，但须通过呼吸作用等转化为 ATP 才能直接驱动生命活动。",
        "方法：抓住 ATP⇄ADP 转化分析能量问题",
        "分析能量相关问题先找“能量从哪里来、到哪里去”：吸能反应常与 ATP 水解偶联，放能反应（如呼吸、光合光反应）为 ATP 合成提供能量。答题时写清 ATP→ADP+Pi+能量 或逆过程，并点明用于主动运输、肌肉收缩、暗反应等具体过程。",
        "主动运输消耗 ATP：载体蛋白构象改变需要能量，ATP 水解为 ADP+Pi，释放的能量驱动物质逆浓度运输。",
        "细胞内的直接能源物质是？",
        ["葡萄糖", "ATP", "脂肪", "淀粉"],
        1,
        "ATP 是直接能源；糖类脂肪等是主要能源，需转化为 ATP 才能直接供能。",
        "常见误区是把葡萄糖当作直接能源。葡萄糖等有机物须经细胞呼吸等过程转化为 ATP，ATP 才是驱动主动运输、肌肉收缩等生命活动的直接能源。",
    ),
    "bio-h-enzyme": C(
        "酶：生物催化剂",
        "酶绝大多数是蛋白质，少数是 RNA（核酶）。酶能显著降低化学反应的活化能，从而加快反应速率，具有高效性、专一性和作用条件较温和的特点。酶活性受温度、pH 影响：过高温度或过酸过碱会使酶变性失活，低温抑制活性但一般不破坏空间结构。",
        "方法：用变量实验分析酶活性",
        "设计酶实验要明确自变量（温度、pH、酶量、底物量）、因变量（产物生成或底物消耗速率）和无关变量。分析曲线时，最适条件处活性最高；超过最适后活性下降常因空间结构被破坏。比较不同处理时注意控制单一变量。",
        "探究过氧化氢酶最适温度时，设置一系列温度梯度，用相同浓度酶和底物，以气泡产生速率或氧气量为因变量。",
        "高温使酶失活的主要原因是？",
        ["底物耗尽", "酶的空间结构被破坏", "酶被分解为氨基酸", "活化能升高"],
        1,
        "高温破坏酶的空间结构导致永久失活；低温通常只是抑制活性。",
        "常见误区是认为低温也会使酶变性失活。低温一般只降低活性，恢复适宜温度后活性可回升；高温、过酸过碱才会破坏空间结构导致失活。",
    ),
    "bio-h-cell-structure": C(
        "细胞：生命活动的基本单位",
        "除病毒外，生物都以细胞为基本单位。细胞有边界（细胞膜）、有相对稳定的内部环境，并能进行物质运输、能量转换和信息传递。认识细胞要从“结构与功能相适应”入手：不同细胞器分工合作，共同完成细胞代谢与生命活动。",
        "方法：结构—功能对应记忆",
        "学习细胞结构时，把每种结构与其主要功能一一对应：如线粒体—有氧呼吸主要场所、叶绿体—光合作用、核糖体—蛋白质合成。比较不同细胞时，先看有无成形细胞核区分原核与真核，再看有无叶绿体、液泡、细胞壁等判断动植物细胞。",
        "心肌细胞线粒体特别多，因为心肌持续收缩需要大量 ATP，体现结构与功能相适应。",
        "除病毒外，生物体结构和功能的基本单位是？",
        ["器官", "细胞", "组织", "分子"],
        1,
        "细胞是除病毒外生物体结构和功能的基本单位。",
        "常见误区是把组织或器官当成基本单位，或认为所有生物都有细胞结构。病毒没有细胞结构；多细胞生物虽有组织器官，基本单位仍是细胞。",
    ),
    "bio-h-cell-membrane": C(
        "细胞膜：流动镶嵌模型",
        "细胞膜主要由磷脂双分子层和蛋白质构成，还含少量糖类。流动镶嵌模型指出：磷脂双分子层构成基本支架，蛋白质分子有的镶在表面、有的部分或全部嵌入、有的贯穿磷脂双分子层；膜具有流动性，且是选择透过性膜。糖蛋白与细胞识别、信息交流密切相关。",
        "方法：用模型解释运输与识别",
        "解释跨膜运输、细胞识别等问题时，紧扣流动镶嵌模型：流动性是膜融合、变形虫运动等的基础；选择透过性依赖磷脂和蛋白质（尤其是载体、通道）的性质。答题先述模型要点，再联系具体功能。",
        "细胞融合实验中不同颜色标记的膜蛋白逐渐均匀分布，证明细胞膜具有流动性。",
        "细胞膜的基本支架是？",
        ["蛋白质分子", "磷脂双分子层", "多糖链", "胆固醇"],
        1,
        "磷脂双分子层是细胞膜的基本支架。",
        "常见误区是认为膜蛋白固定不动，或把细胞膜当成全透/全不透。膜具有流动性，且对物质进出是选择透过的。",
    ),
    "bio-h-organelles": C(
        "细胞器的分工与合作",
        "真核细胞中，线粒体是有氧呼吸主要场所，叶绿体是光合作用场所，核糖体是蛋白质合成机器，内质网参与蛋白质加工与脂质合成，高尔基体与分泌物加工、植物细胞壁形成有关，溶酶体含水解酶，液泡调节植物细胞渗透，中心体与动物细胞有丝分裂有关。各细胞器既分工又合作。",
        "方法：按功能归类细胞器",
        "记忆时可按功能归类：能量代谢（线粒体、叶绿体）、蛋白质合成加工运输（核糖体—内质网—高尔基体）、消化（溶酶体）等。分泌蛋白合成路径是经典考点：核糖体→内质网→高尔基体→细胞膜，该过程需线粒体供能。",
        "分泌蛋白如抗体：附着核糖体合成→内质网粗加工→囊泡→高尔基体再加工→囊泡→胞吐出细胞，线粒体提供能量。",
        "有氧呼吸的主要场所是？",
        ["叶绿体", "线粒体", "核糖体", "液泡"],
        1,
        "线粒体是有氧呼吸的主要场所。",
        "常见误区是把光合作用场所说成线粒体，或搞混分泌蛋白路径顺序。分泌蛋白路径按核糖体→内质网→高尔基体→细胞膜记忆，并注明线粒体供能。",
    ),
    "bio-h-nucleus": C(
        "细胞核：遗传信息库",
        "细胞核是遗传信息库，是细胞代谢和遗传的控制中心。它由核膜、核孔、核仁、染色质等组成。核膜双层，核孔实现核质之间的物质交换与信息交流；染色质由 DNA 和蛋白质构成，是遗传物质的主要载体；核仁与某种 RNA 的合成及核糖体形成有关。",
        "方法：用实验证据理解细胞核功能",
        "理解细胞核功能可结合经典实验：如美西螈核移植、蝾螈受精卵横缢、变形虫切割等，说明细胞核控制生物的性状与代谢。答题时区分“遗传信息库”与“控制中心”两层表述，并联系染色质/染色体是 DNA 的主要载体。",
        "将白色美西螈胚胎的细胞核移入黑色美西螈去核卵细胞中，发育个体表现白色性状，说明性状主要由核基因控制。",
        "遗传物质的主要载体是？",
        ["核糖体", "染色质（染色体）", "细胞质基质", "液泡"],
        1,
        "染色质/染色体由 DNA 和蛋白质组成，是遗传物质的主要载体。",
        "常见误区是认为细胞质决定性状，或把核仁当成遗传信息库。遗传信息主要在细胞核的 DNA 上；核仁与 rRNA 及核糖体形成有关。",
    ),
    "bio-h-prokaryote-eukaryote": C(
        "原核细胞与真核细胞",
        "原核细胞没有由核膜包被的成形细胞核，遗传物质集中在拟核，只有核糖体一种细胞器，代表如细菌、蓝藻、支原体。真核细胞有核膜包被的细胞核，有多种细胞器。两者都有细胞膜、细胞质、核糖体和遗传物质 DNA，说明统一性；结构复杂程度不同体现差异性。",
        "方法：抓“有无核膜”快速判断",
        "判断细胞类型先看有无成形细胞核（核膜）：无则为原核。再记原核仅有核糖体、常有细胞壁（成分与植物不同）。比较题从细胞核、细胞器种类、代表生物列表对照，避免把蓝藻当成真核植物。",
        "蓝藻能光合但无叶绿体，光合色素在光合片层；它无核膜，属于原核生物。",
        "原核细胞与真核细胞最主要的区别是？",
        ["有无细胞壁", "有无核膜包被的细胞核", "有无 DNA", "有无细胞膜"],
        1,
        "最主要区别是有无核膜包被的成形细胞核。",
        "常见误区是把蓝藻、放线菌当成真核，或认为原核没有核糖体和 DNA。原核有核糖体和 DNA，但无成形细胞核、无复杂细胞器。",
    ),
    "bio-h-elements-compounds": C(
        "组成细胞的元素与化合物",
        "组成细胞的元素中，C、H、O、N 含量很多，是基本元素；C 是最基本元素。化合物分无机物（水、无机盐）和有机物（糖类、脂质、蛋白质、核酸）。鲜重中水含量最多，干重中蛋白质通常最多。无机盐多为离子，有重要调节作用。",
        "方法：分鲜重干重、区分大量微量",
        "答题先分清鲜重与干重：鲜重含水最多，干重一般蛋白质最多。元素问题区分大量元素与微量元素，并记住 Fe²⁺是血红蛋白成分、Mg²⁺是叶绿素成分等经典例子。化合物问题先分无机/有机，再对应功能。",
        "缺镁会导致叶绿素合成受阻、叶片发黄，因为 Mg 是叶绿素的组成元素。",
        "细胞鲜重中含量最多的化合物通常是？",
        ["蛋白质", "水", "脂质", "糖类"],
        1,
        "鲜重中水最多；干重中一般蛋白质最多。",
        "常见误区是混淆鲜重与干重的最多成分，或把 C 说成含量最多的元素。含量最多的元素通常是 O（鲜重），最基本元素是 C。",
    ),
    "bio-h-protein-nucleic-acid": C(
        "蛋白质与核酸",
        "蛋白质是生命活动的主要承担者，基本单位是氨基酸，约 20 种，结构通式含氨基、羧基、氢和 R 基连在同一碳上。氨基酸脱水缩合形成肽链，再盘曲折叠成有功能的蛋白质。核酸是遗传信息的携带者，分 DNA 和 RNA，基本单位是核苷酸。",
        "方法：抓通式与脱水缩合计算",
        "判断是否为组成蛋白质的氨基酸看是否符合通式。肽键数=脱去水分子数=氨基酸数—肽链数；至少含氨基/羧基数与肽链数有关。核酸问题分清 DNA（脱氧核糖、T）与 RNA（核糖、U）。",
        "n 个氨基酸形成 1 条肽链，脱去 n−1 分子水，形成 n−1 个肽键，相对分子质量减少 18(n−1)。",
        "氨基酸脱水缩合时，连接两个氨基酸的化学键叫？",
        ["氢键", "肽键", "酯键", "糖苷键"],
        1,
        "氨基酸脱水缩合形成的化学键是肽键。",
        "常见误区是肽键数算成等于氨基酸数，或把 DNA 与 RNA 的碱基搞混。牢记 DNA 特有碱基 T、RNA 特有碱基 U。",
    ),
    "bio-h-sugar-lipid": C(
        "糖类与脂质",
        "糖类是主要的能源物质，分单糖、二糖、多糖。葡萄糖是细胞的重要能源；植物多糖有淀粉、纤维素，动物有糖原。脂质包括脂肪、磷脂和固醇：脂肪是良好的储能物质，磷脂是膜的重要成分，固醇如胆固醇、性激素、维生素 D 有重要功能。",
        "方法：按功能对照记忆种类",
        "能源：葡萄糖、淀粉、糖原；结构：纤维素（细胞壁）、磷脂（膜）；调节：性激素等。区分储能（脂肪）与供能（糖类更常用作主要能源）。遇到“良好储能物质”选脂肪，“主要能源物质”选糖类。",
        "冬眠动物体内脂肪多，因为脂肪碳氢比例高、氧化分解释放能量多，且含结合水较少，是良好的储能物质。",
        "细胞膜上含量丰富、构成膜基本支架的脂质是？",
        ["脂肪", "磷脂", "固醇", "糖原"],
        1,
        "磷脂是细胞膜的重要成分，构成磷脂双分子层支架。",
        "常见误区是把脂肪说成主要能源，或把纤维素当成能源物质。纤维素是结构多糖，一般不能被人体消化供能。",
    ),
    "bio-h-transport-across-membrane": C(
        "物质跨膜运输",
        "被动运输（自由扩散、协助扩散）顺浓度梯度，不消耗能量；主动运输逆浓度梯度，需载体蛋白并消耗能量。自由扩散如水、气体、脂溶性小分子；协助扩散需通道或载体；胞吞胞吐依赖膜流动，运输大分子。自由扩散和协助扩散合称被动运输。",
        "方法：按浓度、能量、载体三要素判断",
        "判断运输方式看三点：是否逆浓度、是否耗能、是否需载体/通道。逆浓度且耗能为主动运输；顺浓度不耗能，有载体/通道为协助扩散，无为自由扩散。曲线题注意载体饱和现象。",
        "小肠吸收葡萄糖一般为主动运输：逆浓度，需载体，消耗能量；红细胞吸收葡萄糖多为协助扩散。",
        "主动运输的特点是？",
        ["顺浓度、不耗能", "逆浓度、需载体和能量", "只需通道蛋白", "只能运大分子"],
        1,
        "主动运输逆浓度梯度，需要载体蛋白并消耗能量。",
        "常见误区是认为凡需载体的都是主动运输。协助扩散也需载体或通道，但不耗能、顺浓度。",
    ),
    "bio-h-endomembrane-system": C(
        "生物膜系统",
        "真核细胞的细胞膜、核膜以及细胞器膜在结构和功能上紧密联系，构成生物膜系统。它使细胞具有广阔的膜面积，为酶提供附着位点，并把细胞分隔成小区室，保证生命活动高效有序进行。分泌蛋白的合成运输体现了膜系统的协调配合。",
        "方法：用分泌蛋白路径理解膜联系",
        "以分泌蛋白为例梳理膜系统联系：内质网膜→囊泡膜→高尔基体膜→囊泡膜→细胞膜，膜面积动态变化。答题强调“结构联系（膜转化）+ 功能联系（分工合作）”。",
        "用同位素标记氨基酸追踪分泌蛋白，可依次在核糖体、内质网、高尔基体检测到放射性，体现内膜系统的功能协作。",
        "生物膜系统的重要意义之一是？",
        ["使细胞没有分区", "提供膜面积并分隔区室，保证有序高效", "只存在于原核生物", "与能量转换无关"],
        1,
        "生物膜系统提供膜面积、附着酶位点并分隔区室，保证生命活动高效有序。",
        "常见误区是把生物膜系统等同于细胞膜，或认为原核也有完整内膜系统。生物膜系统是真核细胞的重要特征。",
    ),
    "bio-h-cellular-respiration": C(
        "细胞呼吸",
        "细胞呼吸是有机物在细胞内氧化分解并释放能量的过程，分有氧呼吸和无氧呼吸。有氧呼吸三阶段：细胞质基质（糖酵解）→线粒体基质（丙酮酸分解）→线粒体内膜（电子传递链），总反应可写成葡萄糖氧化为 CO₂ 和 H₂O 并产生大量 ATP。无氧呼吸在细胞质基质，产物为酒精和 CO₂ 或乳酸。",
        "方法：分阶段记场所、产物与能量",
        "答题按阶段写场所、反应物产物和是否产生 ATP/[H]。比较有氧与无氧：是否彻底氧化、ATP 多少、是否需氧。曲线题注意氧气浓度对两种呼吸的影响及补偿点、饱和点。",
        "酵母菌在无氧时产生酒精和 CO₂，有氧时产生 CO₂ 和 H₂O；可用溴麝香草酚蓝或重铬酸钾等试剂辅助鉴定。",
        "有氧呼吸第三阶段的场所是？",
        ["细胞质基质", "线粒体基质", "线粒体内膜", "叶绿体"],
        2,
        "有氧呼吸第三阶段在线粒体内膜进行。",
        "常见误区是把有氧呼吸全过程都说成在线粒体，或混淆酒精发酵与乳酸发酵的产物。第一阶段在细胞质基质，二三阶段在线粒体。",
    ),
    "bio-h-photosynthesis": C(
        "光合作用",
        "光合作用是绿色植物通过叶绿体，利用光能把 CO₂ 和 H₂O 转化为储存能量的有机物并释放 O₂ 的过程。光反应在类囊体薄膜：水的光解、ATP 和 [H]（NADPH）形成；暗反应在叶绿体基质：CO₂ 固定与 C₃ 还原。光反应为暗反应提供 ATP 和 [H]。",
        "方法：用条件变化推断中间产物",
        "分析光照、CO₂、温度变化对 C₃、C₅、ATP、[H] 含量的影响：停光则 ATP/[H] 下降、C₃ 积累、C₅ 减少；降 CO₂ 则 C₃ 减少、C₅ 积累。答题先判断影响光反应还是暗反应，再推中间产物变化。",
        "突然停止光照，光反应减弱，ATP 和 [H] 减少，C₃ 还原受阻而积累，C₅ 生成减少。",
        "暗反应的场所是？",
        ["类囊体薄膜", "叶绿体基质", "细胞质基质", "线粒体内膜"],
        1,
        "暗反应在叶绿体基质中进行。",
        "常见误区是认为暗反应不需要光反应提供的物质，或把 O₂ 说成暗反应产生。O₂ 来自光反应中水的光解。",
    ),
    "bio-h-photosynthesis-respiration-relation": C(
        "光合与呼吸的关系",
        "光合作用制造有机物并储存能量、释放氧气；呼吸作用分解有机物释放能量供生命活动、产生 CO₂。两者物质上相互依赖：光合为呼吸提供有机物和 O₂，呼吸为光合提供 CO₂ 和中间产物；能量上光合储能、呼吸放能，但呼吸释放的能量不能直接用于光合。",
        "方法：用净光合 = 真光合 − 呼吸分析",
        "测得的通常是净光合。真光合=净光合+呼吸。光照强弱、CO₂ 浓度等影响光合；温度对两者都有影响。光补偿点处光合速率等于呼吸速率，有机物积累为零。",
        "白天净光合为正，有机物积累；夜间只进行呼吸，有机物消耗。作物增产常需提高光能利用、适当增大昼夜温差等。",
        "光补偿点时，下列关系正确的是？",
        ["光合远大于呼吸", "光合速率等于呼吸速率", "只进行呼吸", "不进行代谢"],
        1,
        "光补偿点时光合速率等于呼吸速率，净光合为零。",
        "常见误区是把测得的气体交换量直接当成真正光合速率，忽略呼吸消耗。讨论有机物积累要用净光合。",
    ),
    "bio-h-cell-metabolism": C(
        "细胞代谢总论",
        "细胞代谢是细胞内所有化学反应的统称，包括物质代谢和能量代谢。酶催化、ATP 供能、生物膜系统提供场所，使代谢高效有序。合成代谢（同化作用）储存能量，分解代谢（异化作用）释放能量，二者同时进行、相互联系。",
        "方法：抓酶、ATP、膜三个关键",
        "解释代谢问题围绕三点：谁催化（酶的特性与条件）、能量如何流转（ATP⇄ADP）、反应在何处进行（细胞器与膜系统分区）。把具体过程（光合、呼吸、主动运输）挂到这三框架下分析。",
        "蛋白质合成需核糖体（场所）、酶催化、ATP 供能，并可能经内质网高尔基体加工，体现代谢的有序性。",
        "细胞代谢能够有序进行，主要依赖？",
        ["只有高温", "酶的催化、ATP 供能和膜的区室化", "无规则碰撞", "细胞壁"],
        1,
        "酶、ATP 与生物膜系统共同保证代谢高效有序。",
        "常见误区是把代谢理解成单一反应，或忽视区室化的意义。真核细胞通过生物膜分隔，使不同反应互不干扰又协调配合。",
    ),
    "bio-h-mitosis": C(
        "有丝分裂",
        "有丝分裂是真核生物体细胞增殖的主要方式。细胞周期分分裂间期和分裂期；间期进行 DNA 复制和有关蛋白质合成，时间最长。分裂期分前、中、后、末：前期染色体出现、核膜核仁消失、纺锤体形成；中期着丝粒排列在赤道板；后期着丝粒分裂、姐妹染色单体分离；末期核重建、细胞质分裂。",
        "方法：看染色体行为判断时期",
        "识图抓关键：是否有核膜核仁、染色体是否排列在赤道板、着丝粒是否分裂、是否出现细胞板（植物）或细胞膜中部内陷（动物）。染色体数、染色单体数、DNA 数的变化要分开统计。",
        "中期染色体形态稳定、数目清晰，常用于观察染色体形态和数目。",
        "有丝分裂中，着丝粒分裂发生在？",
        ["前期", "中期", "后期", "末期"],
        2,
        "后期着丝粒分裂，姐妹染色单体成为染色体并移向两极。",
        "常见误区是把染色体数与 DNA 数、染色单体数混为一谈，或认为间期没有变化。间期有 DNA 复制，是染色体加倍（DNA 水平）的关键时期。",
    ),
    "bio-h-cell-cycle": C(
        "细胞周期",
        "连续分裂的细胞从一次分裂完成时开始，到下一次分裂完成时为止，为一个细胞周期。包括分裂间期和分裂期，间期又分 G1、S、G2，S 期进行 DNA 复制。只有连续分裂的细胞才有细胞周期；高度分化的细胞一般不再分裂。",
        "方法：分清时期长短与物质变化",
        "间期远长于分裂期。分析药物作用时，看它抑制 DNA 复制还是抑制纺锤体形成，从而判断细胞滞留在哪一期。计算某期占比可用某期细胞数/总观察细胞数估算。",
        "秋水仙素抑制纺锤体形成，细胞停滞在分裂期，染色体不能移向两极，可用于诱导多倍体。",
        "细胞周期中通常时间最长的是？",
        ["前期", "中期", "分裂间期", "末期"],
        2,
        "分裂间期占比最大，为分裂期进行物质准备。",
        "常见误区是认为所有细胞都有细胞周期，或把分裂期当成最长。高度分化细胞一般离开细胞周期；间期最长。",
    ),
    "bio-h-cell-differentiation": C(
        "细胞分化",
        "细胞分化是个体发育中，细胞在形态、结构和生理功能上发生稳定性差异的过程，本质是基因的选择性表达。分化使多细胞生物中的细胞功能趋向专门化，提高生命活动效率。分化的细胞一般保持遗传物质不变，在一定条件下可能表现全能性。",
        "方法：区分分化、分裂与全能性",
        "分裂增加细胞数量，分化增加细胞种类。全能性指已分化细胞仍含本物种全套遗传信息，条件适宜时可发育成完整个体。植物细胞全能性较易体现；动物细胞核全能性有证据，但已分化动物体细胞整体表现全能性困难。",
        "同一人的口腔上皮细胞与肌细胞遗传物质相同，但形态功能不同，是基因选择性表达的结果。",
        "细胞分化的本质是？",
        ["遗传物质大量丢失", "基因的选择性表达", "细胞数目减少", "细胞膜消失"],
        1,
        "分化本质是基因的选择性表达，遗传物质一般不变。",
        "常见误区是认为分化时基因丢失或突变。正常分化不改变遗传信息总量，而是不同基因表达情况不同。",
    ),
    "bio-h-cell-aging-apoptosis": C(
        "细胞衰老与凋亡",
        "细胞衰老时会发生水分减少、酶活性降低、色素积累、呼吸减慢、膜通透性改变等特征。细胞凋亡是由基因控制的细胞自动结束生命的过程，对胚胎发育、成体稳态有重要意义，与细胞坏死不同。衰老与凋亡都是正常生命现象。",
        "方法：对比凋亡与坏死",
        "凋亡是程序性的、主动的，对机体有利；坏死是不利因素造成的损伤性死亡。个体衰老与细胞衰老相关，但多细胞生物中总有细胞在衰老凋亡，也有新细胞产生。答题抓住“基因控制”“对机体意义”等关键词。",
        "蝌蚪尾的消失、手指间的分隔形成，都与细胞凋亡有关，是发育中的正常过程。",
        "细胞凋亡是指？",
        ["意外损伤导致的死亡", "基因控制的程序性死亡", "细胞无限增殖", "细胞融合"],
        1,
        "凋亡是基因控制的程序性死亡，对机体有积极意义。",
        "常见误区是把凋亡等同于坏死，或认为衰老细胞凋亡都是病理现象。它们是正常生命历程的一部分。",
    ),
}


STYLE = """
<style id="bioh-depth-css">
.bioh-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.bioh-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.24)}
.bioh-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.bioh-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.bioh-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.bioh-depth .bioh-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.bioh-depth .bioh-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="bioh-depth-js">
function biohDepthCheck(button, isCorrect, feedbackId, explanation) {
  var box = button.closest('.module-check');
  if (!box || box.dataset.answered) return;
  box.dataset.answered = '1';
  box.querySelectorAll('button').forEach(function (item) {
    item.disabled = true;
    if (item.dataset.correct === '1') item.classList.add('correct');
  });
  if (!isCorrect) button.classList.add('wrong');
  var feedback = document.getElementById(feedbackId);
  if (feedback) {
    feedback.style.display = 'block';
    feedback.textContent = (isCorrect ? '正确。' : '再想想。') + explanation;
  }
}
</script>
"""


def build_block(cfg: dict) -> str:
    feedback_id = "bioh-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "biohDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false",
            f=feedback_id,
            e=json.dumps(cfg["feedback"], ensure_ascii=False),
        )
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0",
                h=html.escape(handler, quote=True),
                letter=chr(65 + idx),
                opt=html.escape(opt),
            )
        )
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section bioh-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section bioh-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="bioh-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="bioh-feedback" id="{feedback_id}" role="status"></div>
      </div>
    </div>
  </section>
</section>
"""


def upgrade(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="lesson-focus"' in source:
        return False, "already upgraded"
    dpos = -1
    for anchor in ('id="deep-understanding"', 'id="transfer-task"', 'id="posttest"', 'id="summary"'):
        dpos = source.find(anchor)
        if dpos >= 0:
            break
    if dpos < 0:
        return False, "insert anchor not found"
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    insert_at = marker if marker >= 0 else source.rfind("<section", 0, dpos)
    if insert_at < 0:
        return False, "insert marker not found"
    source = source[:insert_at] + build_block(cfg) + "\n" + source[insert_at:]
    if 'id="bioh-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="bioh-depth-js"' not in source:
        source = source.replace("</body>", CHECK_SCRIPT + "\n</body>", 1)
    source = re.sub(r"[ \t]+\n", "\n", source)
    path.write_text(source, encoding="utf-8")
    manifest_path = path.parent / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        changed = False
        for key, value in {"version": COURSE_VERSION, "updated_at": UPDATED_AT}.items():
            if manifest.get(key) != value:
                manifest[key] = value
                changed = True
        if changed:
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    return True, "2 depth modules + metadata"


def main() -> int:
    changed = failed = 0
    for course_id, cfg in COURSES.items():
        ok, msg = upgrade(course_id, cfg)
        if ok:
            changed += 1
            print(f"OK {course_id}: {msg}")
        elif msg == "already upgraded":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed} of {len(COURSES)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
