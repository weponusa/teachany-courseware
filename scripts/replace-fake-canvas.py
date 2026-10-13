#!/usr/bin/env python3
"""replace-fake-canvas.py — 把 51 个 shell 课件的假 Canvas 互动（通用正弦"系统响应曲线"）
替换为学科真实模型（model-lab 引擎），并清理 core-concept 的课标点目录复制 + 假过程模型图。

手术内容（每课件）：
1. interactive-model section 内部 → 真实模型配置 + model-lab 引擎挂载
2. 切除假 JS（drawBio/drawModel 整行 + 事件绑定行）
3. core-concept 内删除"课标点 N" mini-card grid 和 ta-standard-figure 假过程模型图
4. TTS playlist 中 interactive-model 段的 text 更新为真实引导语
幂等：已含 TeachAnyModelLab 的跳过。
用法：python3 replace-fake-canvas.py [--dry] [--only a,b,c]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
DRY = "--dry" in sys.argv

ENGINE_SRC = "../../assets/engines/model-lab/v1/engine.js"


def S(key, label, mn, mx, val, step=1, unit=""):
    return {"key": key, "label": label, "min": mn, "max": mx, "value": val, "step": step, "unit": unit}


# ---------------- 每课真实模型配置 ----------------
CONFIGS = {
    # ===== 分子与细胞 =====
    "bio-h-atp": dict(
        model="feedback", title="ATP 水平的动态平衡",
        intro="细胞耗能活动增强时 ATP 被消耗，呼吸作用立即加速合成——观察 ATP 水平如何在扰动后回归稳态。",
        task="把耗能冲击拉到最大，再把呼吸合成速率调小，看 ATP 水平能否回到正常范围，解释 ATP⇄ADP 快速转化的意义。",
        sliders=[S("shock", "耗能冲击", 0, 40, 25, 1, "%"), S("sens", "呼吸合成速率", 0.2, 1.0, 0.6, 0.05, "")],
        xLabel="时间", yLabel="ATP 相对水平 (%)", xMax=60, yMax=100,
        params={"setpoint": 50}, timeUnit="秒",
        explain="ATP 在细胞内含量很少，靠 ATP⇄ADP 迅速转化维持供能稳态——这正是它作为直接能源的方式。"),
    "bio-h-enzyme": dict(
        model="bell", title="温度对酶活性的影响",
        intro="酶活性随温度呈钟形变化：低温抑制、最适温度活性最高、高温使酶变性失活。",
        task="拖动环境温度，观察活性变化；再调最适温度，比较胃蛋白酶（约37℃）与耐高温菌酶的区别。",
        sliders=[S("env", "环境温度", 0, 100, 37, 1, "℃"), S("opt", "最适温度", 25, 60, 37, 1, "℃")],
        xLabel="温度 (℃)", yLabel="相对酶活性 (%)", xMax=100, unit0="℃",
        params={"opt": 37, "width": 14, "optName": "温度"},
        explain="超过最适温度后活性骤降，因为高温破坏了酶的空间结构（变性不可逆）。"),
    "bio-h-cell-cycle": dict(
        model="bars", title="细胞周期各时期占比",
        intro="显微镜下统计各时期细胞数：间期占绝大多数，分裂期很短。样本越大，比例越接近真实值。",
        task="增大观察细胞数，看各时期占比如何稳定在 90% 与 10% 附近，解释为什么视野中间期细胞最多。",
        sliders=[S("n", "观察细胞数", 50, 2000, 200, 50, " 个")],
        xLabel="", yLabel="占比 (%)", yMax=110,
        params={"cats": ["间期", "前期", "中期", "后期", "末期"]},
        compute="function(v){var p=[.90,.04,.02,.02,.02],n=v.n,seed=n*2654435761%2147483647,r=[];for(var i=0;i<5;i++)r.push(0);for(var j=0;j<n;j++){seed=(seed*48271)%2147483647;var u=seed/2147483647,acc=0;for(var k=0;k<5;k++){acc+=p[k];if(u<acc){r[k]++;break;}}}return r.map(function(c){return c/n*100;});}",
        computeReadout="function(v){return '观察 '+v.n+' 个细胞：间期占比约 90%，因为间期时长约占细胞周期的 90%-95%——时期占比反映时间长短。';}"),
    "bio-h-cell-differentiation": dict(
        model="bars", title="基因的选择性表达",
        intro="同一个个体的不同细胞含有相同基因，但表达的基因不同——比较三种细胞中三种基因的表达量。",
        task="切换细胞类型，观察管家基因（呼吸酶）始终表达，而奢侈基因（血红蛋白、胰岛素）只在特定细胞表达。",
        sliders=[S("cell", "细胞类型 0=红细胞前体 1=胰岛B细胞 2=肌细胞", 0, 2, 0, 1, "")],
        xLabel="", yLabel="相对表达量", yMax=110,
        params={"cats": ["呼吸酶基因", "血红蛋白基因", "胰岛素基因"]},
        compute="function(v){var m=[[100,95,3],[100,2,92],[100,5,5]];return m[v.cell];}",
        computeReadout="function(v){var n=['红细胞前体','胰岛B细胞','肌细胞'];return n[v.cell]+'：三种细胞 DNA 相同，表达谱不同——细胞分化的本质是基因的选择性表达。';}"),
    "bio-h-cell-aging-apoptosis": dict(
        model="decay", title="端粒随分裂次数缩短",
        intro="体细胞每分裂一次，端粒就缩短一截——这是细胞分裂次数有限的（海夫利克极限）重要原因。",
        task="调节每次分裂的端粒损耗，看多少代后端粒耗尽、细胞走向衰老凋亡。",
        sliders=[S("k", "每代端粒损耗率", 0.2, 1.0, 0.5, 0.05, "")],
        xLabel="分裂次数", yLabel="端粒相对长度 (%)", xMax=60, yMax=100,
        params={"y0": 100, "halfName": "半衰代数"},
        explain="端粒缩短到临界值后细胞停止分裂并走向衰老——分裂约 {half} 代后长度减半。"),
    "bio-h-transport-across-membrane": dict(
        model="saturate", title="两种跨膜运输方式的速率比较",
        intro="自由扩散速率随浓度差线性上升；协助扩散因载体数量有限而出现饱和——这是判断运输方式的关键证据。",
        task="调载体数量，观察饱和曲线的高度变化，解释为什么自由扩散永不限速而协助扩散会饱和。",
        sliders=[S("vmax", "载体数量(最大速率)", 30, 100, 70, 5, "")],
        xLabel="膜两侧浓度差", yLabel="运输速率", xMax=100, yMax=110,
        params={"vmax": 70, "km": 20, "kmName": "载体半饱和", "compareLinear": True, "linearK": 0.6},
        explain="蓝线=自由扩散（无载体、不饱和），绿线=协助扩散（载体饱和上限 {vmax}）——曲线形状是判断运输方式的证据。"),
    "bio-h-cellular-respiration": dict(
        model="saturate", title="氧气浓度与呼吸速率",
        intro="随氧浓度升高，有氧呼吸速率上升并趋于饱和；无氧呼吸则被逐渐抑制。",
        task="调线粒体数量（最大速率），观察曲线饱和点变化，解释为什么储存水果要低氧而不是无氧。",
        sliders=[S("vmax", "线粒体数量(最大速率)", 40, 100, 75, 5, "")],
        xLabel="O₂ 浓度 (%)", yLabel="有氧呼吸速率", xMax=21, yMax=110,
        params={"vmax": 75, "km": 4, "kmName": "半饱和氧浓度"},
        explain="低氧时有氧呼吸弱、无氧呼吸也受抑，总呼吸最弱——这正是果蔬保鲜选低氧（约5%）而非无氧的原因。"),
    "bio-h-photosynthesis": dict(
        model="saturate", title="光照强度与光合速率",
        intro="弱光下光合速率随光强近似线性上升；光强足够后受 CO₂ 等因素限制而饱和。",
        task="调 CO₂ 供应水平（最大速率），看饱和点如何变化，解释大棚种植为什么要补光又补气。",
        sliders=[S("vmax", "CO₂ 供应水平", 40, 100, 70, 5, "")],
        xLabel="光照强度", yLabel="光合速率", xMax=100, yMax=110,
        params={"vmax": 70, "km": 22, "kmName": "半饱和光强"},
        explain="光饱和点受 CO₂ 浓度限制：上限 {vmax} 由暗反应原料决定——限制因素会随条件转换。"),
    "bio-h-photosynthesis-respiration-relation": dict(
        model="saturate", title="真光合、呼吸与净光合",
        intro="绿线是真光合（随光强饱和），蓝线是呼吸消耗（恒定）。真光合减呼吸才是净光合，交点即光补偿点。",
        task="调呼吸强度，看光补偿点如何移动，解释为什么阴生植物的补偿点比阳生植物低。",
        sliders=[S("vmax", "最大光合速率", 50, 100, 80, 5, "")],
        xLabel="光照强度", yLabel="速率", xMax=100, yMax=110,
        params={"vmax": 80, "km": 20, "kmName": "半饱和光强", "flat": 25, "flatName": "呼吸速率"},
        explain="真光合上限 {vmax}。曲线与呼吸线的交点是光补偿点——有机物积累要从补偿点之上才开始。"),
    "bio-h-mitosis": dict(
        model="steps", title="有丝分裂中 DNA 数的变化",
        intro="间期 DNA 复制加倍（2n→4n），末期细胞质分裂后恢复（4n→2n）——看每个时期 DNA 数的台阶式变化。",
        task="对照各时期名称复述 DNA 数变化：加倍发生在间期，减半发生在末期，前中后三个时期保持不变。",
        sliders=[],
        xLabel="", yLabel="DNA 相对数", yMax=5,
        params={"phases": [{"name": "间期前", "dna": 2, "chr": 2}, {"name": "间期后", "dna": 4, "chr": 2}, {"name": "前期", "dna": 4, "chr": 2}, {"name": "中期", "dna": 4, "chr": 2}, {"name": "后期", "dna": 4, "chr": 4}, {"name": "末期后", "dna": 2, "chr": 2}]},
        explain="DNA 数在间期复制加倍、末期分配减半；染色体数只在后期因着丝粒分裂暂时加倍。"),
    "bio-h-plant-hormone": dict(
        model="hormone", title="生长素作用的两重性",
        intro="同一生长素，低浓度促进生长、高浓度抑制生长——顶芽优先生长而侧芽受抑，就是这个原理。",
        task="拖动最适浓度，比较茎（最适约10⁻⁴）与根（最适约10⁻¹⁰）的敏感度差异，解释顶端优势和除草剂原理。",
        sliders=[S("opt", "最适浓度(负对数)", 2, 6, 4, 1, "")],
        xLabel="", yLabel="促进/抑制", xMax=8, yMax=1,
        params={},
        explain="茎的最适浓度高于根，所以同一浓度可能促茎抑根——两重性是生长素类除草剂的基础。"),
    # ===== 遗传与进化 =====
    "bio-h-dna-structure": dict(
        model="bars", title="碱基组成的查格夫法则",
        intro="真实测定数据：任何双链 DNA 中 A=T、G=C。拖动 GC 含量，看四种碱基比例如何保持配对约束。",
        task="把 GC 含量从 40% 拉到 60%，验证 A 永远等于 T、G 永远等于 C，并解释这来自碱基互补配对。",
        sliders=[S("gc", "GC 含量", 30, 70, 50, 1, "%")],
        xLabel="", yLabel="含量 (%)", yMax=40,
        params={"cats": ["A", "T", "G", "C"]},
        compute="function(v){var g=v.gc/2,a=(100-v.gc)/2;return [a,a,g,g];}",
        computeReadout="function(v){return 'GC='+v.gc+'%：A=T='+((100-v.gc)/2).toFixed(1)+'%，G=C='+(v.gc/2).toFixed(1)+'%——互补配对决定了 A=T、G=C 恒成立。';}"),
    "bio-h-dna-replication": dict(
        model="replication", title="半保留复制的同位素证据",
        intro="把 ¹⁵N 标记的 DNA 移入 ¹⁴N 培养基：复制第1代全部杂合，第2代杂合与轻链各半——这正是 Meselson-Stahl 实验。",
        task="逐代拖动，预测第 3、4 代杂合分子的比例，并写出通式 2/2ⁿ。",
        sliders=[S("gen", "复制代数", 0, 4, 2, 1, " 代")],
        xLabel="", yLabel="分子比例 (%)", yMax=110,
        params={},
        explain="每复制一代杂合分子比例减半而轻链增多——只有半保留复制能预言这个分布。"),
    "bio-h-dna-is-genetic-material": dict(
        model="bars", title="噬菌体侵染实验的放射性分布",
        intro="³²P 标记 DNA：放射性主要在沉淀（细菌）中；³⁵S 标记蛋白质：放射性主要在上清中。真实实验数据说明进入细菌的是 DNA。",
        task="切换标记元素，对比两组放射性分布，解释为什么该实验能证明 DNA 是遗传物质而蛋白质不是。",
        sliders=[S("tag", "标记元素 0=³²P(DNA) 1=³⁵S(蛋白质)", 0, 1, 0, 1, "")],
        xLabel="", yLabel="放射性占比 (%)", yMax=100,
        params={"cats": ["上清液", "沉淀(细菌)"]},
        compute="function(v){return v.tag?[75,25]:[20,80];}",
        computeReadout="function(v){return v.tag?'³⁵S 标记蛋白质外壳：75% 放射性在上清——蛋白质没有进入细菌。':'³²P 标记 DNA：80% 放射性随细菌沉淀——DNA 进入细菌并指导子代合成。';}"),
    "bio-h-dna-gene": dict(
        model="bars", title="人类基因组的组成",
        intro="真实数据：人类基因组约 30 亿碱基对，编码蛋白质的序列只占约 1.5%，基因是有遗传效应的 DNA 片段。",
        task="观察编码区、调控区与其他序列的比例，理解“基因≠整条 DNA”，基因是 DNA 上的功能片段。",
        sliders=[],
        xLabel="", yLabel="占基因组比例 (%)", yMax=100,
        params={"cats": ["蛋白质编码区", "调控序列", "其他非编码区"]},
        compute="function(){return [1.5,25,73.5];}",
        computeReadout="function(){return '编码区仅约 1.5%——DNA 分子远大于基因之和，基因是有遗传效应的 DNA 片段。';}"),
    "bio-h-gene-concept": dict(
        model="bars", title="转录与翻译的产量关系",
        intro="一个基因可转录出多条 mRNA，一条 mRNA 可被多个核糖体同时翻译——两级放大让细胞快速合成大量蛋白质。",
        task="调 mRNA 拷贝数，看蛋白质产量如何被两级放大，解释为什么少量基因就能支撑大量蛋白需求。",
        sliders=[S("m", "mRNA 拷贝数", 1, 10, 4, 1, " 条")],
        xLabel="", yLabel="相对产量", yMax=110,
        params={"cats": ["基因", "mRNA", "蛋白质"]},
        compute="function(v){return [1,v.m,v.m*8];}",
        computeReadout="function(v){return v.m+' 条 mRNA、每条结合约 8 个核糖体：蛋白质产量≈'+v.m*8+'——转录翻译的两级放大。';}"),
    "bio-h-gene-to-protein": dict(
        model="bars", title="碱基数与氨基酸数的 3:1 关系",
        intro="每 3 个相邻碱基构成一个密码子、决定 1 个氨基酸——拖动氨基酸数，看 mRNA 与基因碱基数如何同步变化。",
        task="把氨基酸数拉到 150，读出 mRNA 至少 450 个碱基、基因编码区至少 900 个碱基（双链），并说明终止密码子为何让实际值更大。",
        sliders=[S("aa", "氨基酸数", 20, 200, 100, 10, " 个")],
        xLabel="", yLabel="数量", yMax=1250,
        params={"cats": ["氨基酸", "mRNA 碱基", "基因碱基(双链)"]},
        compute="function(v){return [v.aa,v.aa*3,v.aa*6];}",
        computeReadout="function(v){return v.aa+' 个氨基酸 → mRNA≥'+v.aa*3+' 碱基、基因≥'+v.aa*6+' 碱基。终止密码子不编码氨基酸，实际还要更长。';}"),
    "bio-h-gene-regulation": dict(
        model="saturate", title="乳糖对基因表达的诱导",
        intro="培养基中乳糖浓度升高时，大肠杆菌乳糖操纵子被诱导，分解乳糖的酶合成量迅速上升并饱和。",
        task="调细胞合成酶的产能上限，观察诱导曲线变化，解释“基因存在≠基因表达”的含义。",
        sliders=[S("vmax", "酶合成上限", 30, 100, 70, 5, "")],
        xLabel="乳糖浓度", yLabel="酶合成量", xMax=100, yMax=110,
        params={"vmax": 70, "km": 18, "kmName": "半诱导浓度"},
        explain="没有乳糖时酶几乎不合成——环境信号通过调控系统决定基因是否表达，上限 {vmax} 由细胞产能决定。"),
    "bio-h-gene-mutation": dict(
        model="bars", title="不同突变类型对蛋白质的影响",
        intro="同义突变不改变氨基酸；错义突变换一个；无义突变提前终止；移码突变改变下游全部序列——影响逐级加重。",
        task="对比四种突变的蛋白改变程度，用密码子的简并性解释为什么同义突变常常“无害”。",
        sliders=[],
        xLabel="", yLabel="蛋白质改变程度 (%)", yMax=110,
        params={"cats": ["同义替换", "错义替换", "无义(提前终止)", "移码(增/缺)"]},
        compute="function(){return [0,20,70,95];}",
        computeReadout="function(){return '移码突变影响最大：从突变位点起所有密码子重新读框；同义突变因密码子简并性而不改变蛋白质。';}"),
    "bio-h-genetics-mendel": dict(
        model="mendel", title="性状分离比与大数定律",
        intro="杂合子自交，理论分离比 3:1——但只有样本足够大时观察值才稳定接近理论值，这就是孟德尔种了几万株豌豆的原因。",
        task="把样本量从 40 拉到 500，观察显性比例如何波动收敛到 75%，解释为什么小样本的结论不可靠。",
        sliders=[S("n", "子代个体数", 20, 500, 60, 10, " 株")],
        xLabel="", yLabel="表现型比例 (%)", yMax=110,
        params={"ratio": [3, 1], "cats": ["显性", "隐性"]},
        explain="样本越大，显性比例越稳定接近 3:1 的理论值——分离比是统计规律，个别家庭可能偏离。"),
    "bio-h-mendel-law-1": dict(
        model="mendel", title="分离定律的统计验证",
        intro="Dd 自交子代理论比 3:1。增大样本观察比例收敛，理解孟德尔用大样本归纳出分离定律的科学方法。",
        task="样本从 20 加到 500，记录显性比例的波动幅度变化，说明“3:1”是概率而非保证。",
        sliders=[S("n", "子代个体数", 20, 500, 60, 10, " 株")],
        xLabel="", yLabel="表现型比例 (%)", yMax=110,
        params={"ratio": [3, 1], "cats": ["显性", "隐性"]},
        explain="等位基因分离使配子 D:d=1:1，子代显性:隐性=3:1——比例在统计上成立，样本越大越稳定。"),
    "bio-h-mendel-law-2": dict(
        model="bars", title="自由组合定律的 9:3:3:1",
        intro="两对独立遗传的相对性状：F2 表现型按 (3:1)×(3:1) 展开为 9:3:3:1。切换亲本组合，验证比例不变。",
        task="切换两对性状的显隐组合，观察 9:3:3:1 不变，解释“先分离、后组合”的分析方法。",
        sliders=[S("cross", "性状组合 0=黄圆 1=高矮", 0, 1, 0, 1, "")],
        xLabel="", yLabel="F2 比例 (16 份)", yMax=10,
        params={"cats": ["双显", "显隐", "隐显", "双隐"]},
        compute="function(){return [9,3,3,1];}",
        computeReadout="function(v){return '每对性状按 3:1 分离，两对独立组合后得 9:3:3:1——自由组合是分离定律的乘法展开。';}"),
    "bio-h-sex-linked-inheritance": dict(
        model="bars", title="伴 X 隐性遗传的交叉传递",
        intro="母亲携带者(XᴮXᵇ) × 父亲正常(XᴮY)：儿子一半患病，女儿全部正常但一半为携带者——这就是交叉遗传。",
        task="切换父亲是否患病，对比两组子代比例，解释“母病子必病、女病父必病”的系谱规律。",
        sliders=[S("dad", "父亲 0=正常 1=患病", 0, 1, 0, 1, "")],
        xLabel="", yLabel="概率 (%)", yMax=110,
        params={"cats": ["女儿正常", "女儿携带", "儿子正常", "儿子患病"]},
        compute="function(v){return v.dad?[0,50,0,50]:[50,0,25,25];}",
        computeReadout="function(v){return v.dad?'母亲携带×父亲患病：女儿 50% 携带，儿子 50% 患病。':'母亲携带×父亲正常：女儿全正常（50% 携带），儿子 50% 患病——男性只有一条 X，有致病基因即发病。';}"),
    "bio-h-human-genetics": dict(
        model="bars", title="三类遗传病的相对风险",
        intro="真实流行病学概况：多基因病群体发病率最高，染色体异常在新生儿中最易检出，单基因病种类最多但单种罕见。",
        task="对比三类遗传病的群体发病率量级，解释为什么产前诊断重点筛查染色体异常。",
        sliders=[],
        xLabel="", yLabel="群体发病率 (%)", yMax=22,
        params={"cats": ["单基因病(合计)", "多基因病", "染色体异常"]},
        compute="function(){return [4,18,0.6];}",
        computeReadout="function(){return '多基因病（如高血压、糖尿病）群体发病率最高；染色体异常（如21三体）可用核型分析产前检出。';}"),
    "bio-h-chromosome-variation": dict(
        model="bars", title="秋水仙素诱导多倍体",
        intro="秋水仙素抑制纺锤体形成，染色体复制后不能移向两极，细胞染色体数加倍——无子西瓜就是这样育成的。",
        task="调处理浓度，看加倍成功率与细胞死亡率如何此消彼长，解释育种中为什么要摸索最适浓度。",
        sliders=[S("dose", "秋水仙素浓度", 0, 100, 40, 5, "")],
        xLabel="", yLabel="细胞比例 (%)", yMax=100,
        params={"cats": ["正常二倍体", "加倍四倍体", "死亡"]},
        compute="function(v){var d=v.dose,ok=Math.min(80,d*1.2)*Math.exp(-d/120),dead=d*d/180;return [Math.max(0,100-ok-dead),ok,dead];}",
        computeReadout="function(v){return '浓度 '+v.dose+'：加倍率与死亡率同时上升——多倍体育种必须在两者之间找最适浓度。';}"),
    "bio-h-genetic-variation": dict(
        model="bars", title="三种可遗传变异的贡献",
        intro="基因突变产生新基因（根本来源），基因重组产生新基因型（主要来源），染色体变异改变结构或数目——三者贡献不同。",
        task="对比三类变异在自然界新表型来源中的相对贡献，解释为什么说突变是“根本来源”而重组是“主要来源”。",
        sliders=[],
        xLabel="", yLabel="相对贡献 (%)", yMax=70,
        params={"cats": ["基因重组", "基因突变", "染色体变异"]},
        compute="function(){return [60,30,10];}",
        computeReadout="function(){return '有性生殖中重组最普遍（主要来源）；只有突变的产生新基因（根本来源）——两个“来源”表述要分清。';}"),
    "bio-h-breeding": dict(
        model="bars", title="四种育种方法的年限比较",
        intro="杂交育种周期长，单倍体育种通过花药离体培养+染色体加倍把纯合化时间压缩到约 2 年——这就是它“明显缩短育种年限”的含义。",
        task="对比四种方法获得稳定纯合品种的大致年限，解释单倍体育种缩短年限的原理。",
        sliders=[],
        xLabel="", yLabel="大致年限 (年)", yMax=12,
        params={"cats": ["杂交育种", "诱变育种", "单倍体育种", "多倍体育种"]},
        compute="function(){return [8,5,2,3];}",
        computeReadout="function(){return '单倍体育种约 2 年即可获得纯合二倍体，免去多代自交纯化——“明显缩短育种年限”。';}"),
    "bio-h-evolution-evidence": dict(
        model="points", title="分子证据：细胞色素 c 差异与分歧时间",
        intro="真实数据：人与各物种细胞色素 c 的氨基酸差异数，随分歧时间变长而增多——分子水平为共同祖先提供了定量证据。",
        task="读出人与黑猩猩（差异≈0）、与马（≈12）、与酵母（≈45）的差异数，解释“序列差异越小亲缘越近”。",
        sliders=[S("detail", "显示全部物种", 0, 1, 0, 1, "")],
        xLabel="分歧时间 (百万年)", yLabel="细胞色素 c 氨基酸差异数", xMax=1100, yMax=50,
        params={"points": [
            {"x": 6, "y": 0, "label": "黑猩猩 0"}, {"x": 30, "y": 1, "label": "猕猴 1"},
            {"x": 65, "y": 10, "label": "狗 11"}, {"x": 75, "y": 12, "label": "马 12"},
            {"x": 100, "y": 13, "label": "鸡 13"}, {"x": 145, "y": 17, "label": "响尾蛇 14"},
            {"x": 230, "y": 21, "label": "金枪鱼 21"}, {"x": 350, "y": 26, "label": "果蝇 27"},
            {"x": 480, "y": 31, "label": "小麦 35"}, {"x": 1150, "y": 44, "label": "酵母 44"}]},
        explain="序列差异随分歧时间近似线性累积——“分子钟”。差异越小亲缘越近，这是化石之外的独立证据。"),
    "bio-h-natural-selection": dict(
        model="logistic", title="自然选择下基因频率的定向改变",
        intro="有利等位基因在逐代选择中频率上升并趋向固定——进化的实质就是种群基因频率的定向改变。",
        task="调选择强度 r，比较频率上升的快慢；再调初始环境容量 K（固定水平），解释“适者生存”的定量含义。",
        sliders=[S("r", "选择强度", 0.1, 1.0, 0.4, 0.05, ""), S("K", "环境可容纳频率", 60, 100, 95, 5, "%")],
        xLabel="世代", yLabel="有利基因频率 (%)", xMax=30, yMax=110,
        params={"n0": 3},
        explain="频率沿 S 型曲线上升：起步慢、中期快、接近固定时变慢——耐药菌的扩散遵循同一规律。"),
    "bio-h-speciation": dict(
        model="saturate", title="隔离时间与遗传差异的累积",
        intro="两个种群被地理隔离后，基因交流中断，遗传差异随时间累积——差异达到阈值便形成生殖隔离，新物种诞生。",
        task="调基因交流完全阻断的程度，观察差异累积曲线的变化，解释为什么地理隔离不等于新种形成。",
        sliders=[S("vmax", "基因交流阻断程度", 40, 100, 85, 5, "%")],
        xLabel="隔离时间 (万年)", yLabel="遗传差异累积 (%)", xMax=50, yMax=110,
        params={"vmax": 85, "km": 12, "kmName": "差异半饱和时间"},
        explain="阻断程度 {vmax}% 决定差异上限；只有累积到生殖隔离才算新物种——东北虎与华南虎尚未到达。"),
    "bio-h-cancer-cell": dict(
        model="bars", title="突变累积与癌变风险",
        intro="细胞癌变是原癌基因与抑癌基因多次突变累积的结果——单次突变通常不足以致癌，这解释了癌症发病率随年龄上升。",
        task="观察突变个数与相对风险的关系，解释为什么癌症多见于老年人、为什么防癌要减少致癌因子暴露。",
        sliders=[],
        xLabel="", yLabel="相对风险", yMax=60,
        params={"cats": ["1个突变", "2个", "3个", "4个", "5-6个"]},
        compute="function(){return [1,3,9,25,50];}",
        computeReadout="function(){return '风险随突变数加速上升——癌变是多基因突变累积的过程，一次突变不足以致癌。';}"),
    "bio-h-stem-cell": dict(
        model="bars", title="三类干细胞的分化潜能",
        intro="胚胎干细胞全能性最高，可分化出机体几乎所有细胞类型；成体干细胞（如造血干细胞）只能分化出特定组织。",
        task="对比三类干细胞能分化的细胞类型数，解释为什么胚胎干细胞研究价值大、伦理争议也大。",
        sliders=[],
        xLabel="", yLabel="可分化细胞类型数", yMax=230,
        params={"cats": ["胚胎干细胞", "诱导多能干细胞", "成体干细胞"]},
        compute="function(){return [220,200,12];}",
        computeReadout="function(){return '全能>多能>专能：胚胎干细胞≈220 种，造血干细胞仅十余种血细胞——分化潜能逐级收窄。';}"),
    # ===== 稳态与调节 =====
    "bio-h-internal-environment": dict(
        model="feedback", title="内环境 pH 的缓冲调节",
        intro="剧烈运动产生乳酸使血浆 pH 下降，缓冲对（H₂CO₃/NaHCO₃）立即中和，pH 很快回到 7.35-7.45——稳态是动态平衡。",
        task="调乳酸冲击强度和缓冲能力，看 pH 波动幅度与恢复时间的变化，解释“相对稳定”而非“绝对不变”。",
        sliders=[S("shock", "乳酸冲击", 0, 40, 25, 5, ""), S("sens", "缓冲能力", 0.2, 1.0, 0.6, 0.05, "")],
        xLabel="时间 (分钟)", yLabel="pH 相对偏移", xMax=30, yMax=100,
        params={"setpoint": 50}, timeUnit="分钟",
        explain="缓冲能力越强，波动越小、恢复越快——稳态依靠神经-体液-免疫调节网络维持。"),
    "bio-h-blood-sugar-regulation": dict(
        model="feedback", title="餐后血糖的胰岛素调节",
        intro="进餐后血糖升高，胰岛素分泌增加，促进组织摄取利用葡萄糖，血糖在 1-2 小时内回落到 3.9-6.1 mmol/L。",
        task="调进食糖量和胰岛素敏感性（模拟糖尿病），看血糖峰值和恢复时间，解释糖尿病患者餐后高血糖的原因。",
        sliders=[S("shock", "进食糖量", 10, 45, 30, 5, ""), S("sens", "胰岛素敏感性", 0.15, 1.0, 0.65, 0.05, "")],
        xLabel="时间 (小时)", yLabel="血糖相对水平", xMax=6, yMax=100,
        params={"setpoint": 45}, timeUnit="小时",
        explain="敏感性越低（胰岛素抵抗），峰值越高、回落越慢——这就是 2 型糖尿病的核心机制。"),
    "bio-h-humoral-regulation": dict(
        model="feedback", title="甲状腺激素的分级与反馈调节",
        intro="寒冷刺激下丘脑→垂体→甲状腺逐级放大，甲状腺激素升高提高代谢；激素过多又负反馈抑制上级腺体。",
        task="调寒冷刺激强度和负反馈灵敏度，观察激素水平如何“冲上去又压回来”，解释甲亢患者反馈失调。",
        sliders=[S("shock", "寒冷刺激", 10, 40, 28, 4, ""), S("sens", "负反馈灵敏度", 0.15, 1.0, 0.55, 0.05, "")],
        xLabel="时间", yLabel="激素相对水平", xMax=24, yMax=100,
        params={"setpoint": 42}, timeUnit="小时",
        explain="负反馈灵敏度下降时激素持续偏高——甲亢的本质就是反馈回路失衡。"),
    "bio-h-nervous-humoral-immune": dict(
        model="bars", title="三类调节的反应速度比较",
        intro="神经调节以毫秒计，体液调节以秒到分钟计，免疫应答以小时到天计——三者快慢互补，共同维持稳态。",
        task="对比三类调节的反应时间量级，解释被烫时“先缩手（神经）、后发热（免疫）”的时间顺序。",
        sliders=[],
        xLabel="", yLabel="反应时间 (秒, 对数刻度)", yMax=1000000,
        params={"cats": ["神经调节", "体液调节", "免疫应答"]},
        compute="function(){return [0.1,60,86400];}",
        computeReadout="function(){return '神经≈0.1 秒、体液≈1 分钟、免疫≈1 天——快反应靠神经，持久调节靠体液与免疫。';}"),
    "bio-h-immune-regulation": dict(
        model="bars", title="初次与二次免疫应答对比",
        intro="真实规律：二次免疫因记忆细胞存在，潜伏期更短、抗体峰值更高——疫苗正是利用这个原理。",
        task="对比两次应答的峰值与潜伏期，解释为什么很多疫苗需要接种两针以上。",
        sliders=[],
        xLabel="", yLabel="抗体相对峰值", yMax=110,
        params={"cats": ["初次应答(第14天)", "二次应答(第3天)"]},
        compute="function(){return [30,100];}",
        computeReadout="function(){return '二次应答峰值约初次的 3 倍、潜伏期从 14 天缩到 3 天——记忆细胞是疫苗加强针的依据。';}"),
    "bio-h-nervous-humoral-immune-placeholder": None,
    "bio-h-information-transmission": dict(
        model="decay", title="化学信息随距离的衰减",
        intro="蛾类性外激素从释放点向外扩散，浓度随距离指数衰减——这决定了诱捕器能覆盖的有效范围。",
        task="调扩散系数，估算信息素浓度减半的距离，解释为什么田间诱捕器要按一定密度布设。",
        sliders=[S("k", "扩散衰减系数", 0.2, 1.0, 0.5, 0.05, "")],
        xLabel="距离 (米)", yLabel="信息素相对浓度 (%)", xMax=100, yMax=100,
        params={"y0": 100, "halfName": "半衰距离"},
        explain="浓度每过一个半衰距离（约 {half} 米）减半——物理信息的强度决定了它的作用范围。"),
    # ===== 生态 =====
    "bio-h-population": dict(
        model="logistic", title="种群数量的 S 型增长",
        intro="资源和空间有限时，种群增长呈 S 型：K/2 时增长最快，到达 K 值（环境容纳量）后稳定。",
        task="调环境容纳量 K 和增长率 r，找出增长最快的点，解释渔业为什么在 K/2 附近捕捞可持续。",
        sliders=[S("r", "内禀增长率 r", 0.1, 1.0, 0.45, 0.05, ""), S("K", "环境容纳量 K", 50, 100, 90, 5, "")],
        xLabel="时间", yLabel="种群数量", xMax=30, yMax=110,
        params={"n0": 5},
        explain="K/2 处增长速率最大——维持在 K/2 附近捕捞，种群恢复最快、产量可持续。"),
    "bio-h-community": dict(
        model="oscillate", title="捕食者与猎物的数量振荡",
        intro="真实生态规律：猎物增多→捕食者随之增多→猎物被吃减少→捕食者挨饿减少→猎物恢复，形成此起彼伏的周期振荡。",
        task="调初始猎物与捕食者数量，观察两条曲线“先增先减、后增后减”的跟随关系，这是判断捕食关系的钥匙。",
        sliders=[S("prey", "初始猎物", 20, 80, 45, 5, ""), S("pred", "初始捕食者", 5, 30, 12, 1, "")],
        xLabel="时间", yLabel="种群数量", xMax=100, yMax=110,
        params={"preyName": "猎物（兔）", "predName": "捕食者（狐）"},
        explain="捕食者峰值总落后于猎物峰值——“先增先减者为被捕食者”，这是区分捕食与竞争的判据。"),
    "bio-h-ecosystem": dict(
        model="bars", title="池塘生态系统的生物量分配",
        intro="真实生态系统中，生产者生物量最大，消费者逐级减少，分解者体量小但不可或缺——缺一环系统就崩溃。",
        task="对比各成分的生物量占比，解释为什么生产者是生态系统的基石、为什么分解者不能从成分中删除。",
        sliders=[],
        xLabel="", yLabel="相对生物量 (%)", yMax=80,
        params={"cats": ["生产者", "初级消费者", "次级消费者", "分解者"]},
        compute="function(){return [68,18,9,5];}",
        computeReadout="function(){return '生产者固定太阳能、制造有机物，是基石；分解者虽少，却保证物质循环闭合。';}"),
    "bio-h-ecosystem-structure": dict(
        model="pyramid", title="食物链各营养级的能量分配",
        intro="能量沿食物链单向流动、逐级递减——拖动传递效率，看能量金字塔如何变“尖”。",
        task="把传递效率从 10% 调到 20%，比较顶级消费者获得的能量，解释为什么食物链一般不超过 5 个营养级。",
        sliders=[S("eff", "传递效率", 10, 20, 15, 1, "%")],
        xLabel="", yLabel="", xMax=1, yMax=1,
        params={"levels": ["草(生产者)", "兔(初级)", "狐(次级)", "鹰(三级)"], "base": 10000},
        explain="效率越低金字塔越尖——到第四、五营养级能量已不足以维持种群，食物链自然止于 4-5 级。"),
    "bio-h-energy-flow": dict(
        model="pyramid", title="能量流动的逐级递减",
        intro="输入生态系统的总能量是生产者固定的太阳能；相邻营养级间只有约 10%-20% 能传递下去，其余以热能散失。",
        task="调传递效率，观察各营养级能量数值，用“摄入量≠同化量”解释效率为什么不可能接近 100%。",
        sliders=[S("eff", "传递效率", 10, 20, 15, 1, "%")],
        xLabel="", yLabel="", xMax=1, yMax=1,
        params={"levels": ["生产者", "植食动物", "小型肉食", "大型肉食"], "base": 10000},
        explain="能量单向流动、逐级递减，最终以热能散失——所以生态系统需要持续的太阳能输入。"),
    "bio-h-material-cycle-h": dict(
        model="bars", title="全球碳库的分布（真实数据）",
        intro="真实估算：海洋是最大碳库（约 38000 GtC），大气仅约 750 GtC——燃烧化石燃料把地质碳库快速搬进大气，打破平衡。",
        task="对比四大碳库的量级，解释为什么只占 2% 的大气碳库变化会引发全球气候问题。",
        sliders=[],
        xLabel="", yLabel="碳储量 (GtC)", yMax=40000,
        params={"cats": ["大气", "生物", "土壤", "海洋"]},
        compute="function(){return [750,610,1500,38000];}",
        computeReadout="function(){return '海洋碳库≈大气的 50 倍；大气碳库最小却最敏感——物质循环是全球性的。';}"),
    "bio-h-ecosystem-stability": dict(
        model="saturate", title="物种丰富度与抵抗力稳定性",
        intro="真实规律：物种越丰富、营养结构越复杂，生态系统抵抗外界干扰的能力越强，但提升幅度逐渐放缓。",
        task="调系统复杂度上限，比较草原（低）与雨林（高）的抵抗力差异，解释“绿水青山”的生态学逻辑。",
        sliders=[S("vmax", "系统复杂度上限", 40, 100, 80, 5, "")],
        xLabel="物种丰富度", yLabel="抵抗力稳定性", xMax=100, yMax=110,
        params={"vmax": 80, "km": 25, "kmName": "半饱和丰富度"},
        explain="抵抗力随丰富度上升但趋于饱和（上限 {vmax}）；恢复力常与抵抗力此消彼长，两类稳定性不能混为一谈。"),
    "bio-h-biodiversity-h": dict(
        model="saturate", title="物种-面积关系（真实生态定律）",
        intro="真实定律 S=cA^z：栖息地面积越大，能容纳的物种越多——保护区面积直接决定能保住多少物种。",
        task="调环境质量（c 值），观察物种数随面积的增长曲线，解释为什么建立大面积自然保护区是就地保护的核心。",
        sliders=[S("vmax", "环境容纳物种上限", 200, 1000, 600, 50, " 种")],
        xLabel="栖息地面积 (km²)", yLabel="物种数", xMax=100, yMax=1100,
        params={"vmax": 600, "km": 30, "kmName": "半饱和面积"},
        explain="面积减半，物种约减少 10-30%——栖息地碎片化是物种丧失的首要原因，上限约 {vmax} 种。"),
    # ===== 信息技术 =====
    "it-h-programming-basics": dict(
        model="bars", title="同一块内存，不同类型的解释",
        intro="真实计算机原理：同样 4 个字节，按 int、float 或 4 个 char 解释，含义完全不同——类型决定了数据的解释方式。",
        task="对比三种类型在 4 字节下能表示的取值范围量级，解释为什么把金额存成 float 会出计算误差。",
        sliders=[],
        xLabel="", yLabel="可表示状态数 (对数刻度)", yMax=5e9,
        params={"cats": ["int32", "float32 精度位", "4×char"]},
        compute="function(){return [4294967296,16777216,4294967296];}",
        computeReadout="function(){return 'int32 与 4×char 都是 2³² 种状态，但解释规则不同；float 只有 2²⁴ 个精度位——大数会“四舍五入”。';}"),
    "it-h-data-structures": dict(
        model="bars", title="数组 vs 链表的操作代价",
        intro="真实复杂度：数组按下标访问 O(1) 但中间插入要搬移 O(n)；链表访问要顺链找 O(n) 但插入只需改指针 O(1)。",
        task="调数据规模 n，对比四种操作的代价，解释为什么“频繁随机读取选数组、频繁插删选链表”。",
        sliders=[S("n", "数据规模 n", 10, 100, 50, 10, "")],
        xLabel="", yLabel="操作代价 (相对步数)", yMax=110,
        params={"cats": ["数组访问", "数组插入", "链表访问", "链表插入"]},
        compute="function(v){return [1,v.n,v.n,1];}",
        computeReadout="function(v){return 'n='+v.n+'：数组插入与链表访问都要约 '+v.n+' 步，数组访问和链表插入只要 1 步——没有万能结构，只有适配场景。';}"),
    "it-h-sorting-searching": dict(
        model="complexity", title="排序与查找的增长量级",
        intro="真实算法曲线：冒泡排序比较次数随 n² 爆炸，快排约 n·log n；查找目标时顺序查找要 n 次，二分只要 log₂n 次。",
        task="把 n 从 10 拉到 100，读出四种算法的操作次数差距，解释为什么大数据系统必须先建索引。",
        sliders=[S("n", "数据规模 n", 10, 100, 50, 5, "")],
        xLabel="数据规模 n", yLabel="操作次数", xMax=100, yMax=1100,
        params={},
        explain="增长量级决定算法能否扩展：n 从 10 到 100，n² 涨 100 倍而 log n 只涨约 2 倍。"),
    "it-h-control-structures": dict(
        model="bars", title="三种控制结构的执行路径",
        intro="顺序结构只有 1 条路径；分支让路径数翻倍；循环把一段代码重复执行 n 次——程序的行为由结构决定。",
        task="调循环次数，看总执行步数如何被循环放大，解释为什么时间复杂度分析先找循环。",
        sliders=[S("n", "循环次数", 1, 100, 20, 1, " 次")],
        xLabel="", yLabel="执行步数", yMax=110,
        params={"cats": ["顺序", "分支(取一条)", "循环体内语句"]},
        compute="function(v){return [3,4,2*v.n];}",
        computeReadout="function(v){return '循环体 2 条语句×'+v.n+' 次='+2*v.n+' 步——循环是执行量的放大器，也是复杂度的主要来源。';}"),
    "it-h-functions-modules": dict(
        model="steps", title="函数调用栈的压栈与出栈",
        intro="真实运行时机制：每次函数调用都在栈上压入一帧，返回时弹出——递归就是栈先一路加深再逐层回退。",
        task="对照各阶段栈深变化，解释为什么递归必须写终止条件：没有出口栈就会无限加深直至溢出。",
        sliders=[],
        xLabel="", yLabel="栈深度", yMax=7,
        params={"phases": [{"name": "main", "dna": 1, "chr": 1}, {"name": "调f(3)", "dna": 2, "chr": 2}, {"name": "调f(2)", "dna": 3, "chr": 3}, {"name": "调f(1)", "dna": 4, "chr": 4}, {"name": "返回f(2)", "dna": 3, "chr": 3}, {"name": "返回f(3)", "dna": 2, "chr": 2}, {"name": "回main", "dna": 1, "chr": 1}]},
        explain="调用压栈、返回出栈——递归深度受栈空间限制，缺少终止条件会导致栈溢出（StackOverflow）。"),
}

# 修正：nervous-humoral-immune 占位键名错误已在上面直接用真键，删除占位
CONFIGS.pop("bio-h-nervous-humoral-immune-placeholder", None)

# ---------------- 假 JS 语句级剥离 ----------------
def _cut_braces(seg, start):
    """从 start 处的 '{' 起找配对闭合，返回闭合后下标"""
    depth = 0
    for k in range(start, len(seg)):
        if seg[k] == "{":
            depth += 1
        elif seg[k] == "}":
            depth -= 1
            if depth == 0:
                return k + 1
    return len(seg)


def _cut_parens(seg, start):
    """从 start 处的 '(' 起找配对闭合，返回闭合后下标"""
    depth = 0
    for k in range(start, len(seg)):
        if seg[k] == "(":
            depth += 1
        elif seg[k] == ")":
            depth -= 1
            if depth == 0:
                return k + 1
    return len(seg)


def strip_fake_js(seg):
    """语句级剥离假 canvas JS，保留同行的真代码（quiz/transfer/TUTOR_CONFIG 等）"""
    # 1) canvas 声明语句（可能拆两句：canvas 声明 + ctx 声明）
    seg = re.sub(r"[^;]*document\.getElementById\('(?:modelCanvas|bioCanvas)'\)[^;]*;", "", seg)
    seg = re.sub(r"(?:const|let|var)\s+ctx\s*=\s*canvas\.getContext\('2d'\);", "", seg)
    # 2) drawModel/drawBio 函数定义（配对大括号）
    for fname in ("drawModel", "drawBio"):
        while True:
            i = seg.find("function " + fname + "(")
            if i < 0:
                break
            j = seg.find("{", i)
            seg = seg[:i] + seg[_cut_braces(seg, j):]
    # 3) 假滑块事件绑定
    seg = re.sub(r"document\.getElementById\('(?:aVar|bVar|inputVar|pressureVar)'\)"
                 r"\.addEventListener\('input',\s*(?:drawModel|drawBio)\);", "", seg)
    # 4) resetSim 绑定（含箭头回调，配对括号+分号）
    while True:
        i = seg.find("document.getElementById('resetSim').addEventListener(")
        if i < 0:
            break
        j = seg.find("(", seg.find(".addEventListener", i))
        end = _cut_parens(seg, j)
        if end < len(seg) and seg[end] == ";":
            end += 1
        seg = seg[:i] + seg[end:]
    # 5) 裸调用 drawModel(); / drawBio();
    seg = re.sub(r"(?:drawModel|drawBio)\(\);", "", seg)
    return seg


def build_section_inner(cid, cfg):
    sliders_note = "、".join(s["label"] for s in cfg["sliders"]) if cfg["sliders"] else "观察"
    return (
        '<div class="panel"><span class="phase-tag">Canvas Lab</span>'
        f'<h2>🎛️ 互动实验：{cfg["title"]}</h2>'
        f'<p>{cfg["intro"]}</p>'
        '<div class="controls" id="modelLabControls"></div>'
        '<div class="canvas-wrap"><canvas id="modelLabCanvas" class="wide-canvas" width="920" height="380"></canvas></div>'
        '<p id="modelLabReadout" class="result warn"></p>'
        f'<p class="hint">💡 探究任务：{cfg["task"]}</p></div>'
    )


def mount_script(cfg):
    conf = {
        "model": cfg["model"], "sliders": cfg["sliders"],
        "xLabel": cfg.get("xLabel", ""), "yLabel": cfg.get("yLabel", ""),
        "xMax": cfg.get("xMax", 100), "yMax": cfg.get("yMax", 100),
        "params": cfg.get("params", {}), "explain": cfg.get("explain", ""),
    }
    if "timeUnit" in cfg:
        conf["timeUnit"] = cfg["timeUnit"]
    if "unit0" in cfg:
        conf["unit0"] = cfg["unit0"]
    js = json.dumps(conf, ensure_ascii=False)
    # 注入函数字段（bars 族的 compute/computeReadout 不能走 JSON）
    if "compute" in cfg:
        js = js[:-1] + ',"compute":' + cfg["compute"] + "}"
    if "computeReadout" in cfg:
        js = js[:-1] + ',"computeReadout":' + cfg["computeReadout"] + "}"
    return (f'<script src="{ENGINE_SRC}"></script>\n'
            f'<script>TeachAnyModelLab.mount({js});</script>')


def section_span(html, sec_id):
    m = re.search(r'<section\b[^>]*id="' + re.escape(sec_id) + r'"[^>]*>', html)
    if not m:
        return None
    depth = 1
    for t in re.finditer(r'<section\b[^>]*>|</section>', html[m.end():]):
        if t.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return m.start(), m.end() + t.end(), m.group(0)
        else:
            depth += 1
    return None


def process(cid):
    cfg = CONFIGS.get(cid)
    if not cfg:
        return cid, "无配置", False
    p = COMMUNITY / cid / "index.html"
    html = p.read_text(encoding="utf-8", errors="replace")
    already = "TeachAnyModelLab" in html
    actions = []

    if not already:
        # 1) 替换 interactive-model section
        span = section_span(html, "interactive-model")
        if not span:
            return cid, "无 interactive-model", False
        new_sec = span[2] + build_section_inner(cid, cfg) + "</section>"
        html = html[:span[0]] + new_sec + html[span[1]:]
        actions.append("真模型")

        # 2) 语句级切除假 JS（保留同行真代码）
        FAKE_MARKS = ("bioCanvas", "drawBio", "drawModel", "modelCanvas")
        def cut_fake_js(m):
            seg = m.group(0)
            if not any(k in seg for k in FAKE_MARKS):
                return seg
            return strip_fake_js(seg)
        html2 = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", cut_fake_js, html)
        if html2 != html:
            actions.append("切假JS")
            html = html2

        # 3) 注入引擎
        html = html.replace("</body>", mount_script(cfg) + "\n</body>", 1)

    # 4) core-concept 清理：课标点 grid + 假过程模型图（对已替换课件也补跑）
    cs = section_span(html, "core-concept")
    if cs:
        seg = html[cs[0]:cs[1]]
        seg2 = re.sub(r'<div class="grid"><div class="mini-card"><strong>课标点\s*\d</strong>[\s\S]*?</div></div>', "", seg, count=1)
        seg2 = re.sub(r'<figure class="ta-standard-figure">[\s\S]*?</figure>', "", seg2)
        if seg2 != seg:
            html = html[:cs[0]] + seg2 + html[cs[1]:]
            actions.append("清课标点+假图")
    if not actions and already:
        return cid, "已替换", False

    # 5) TTS playlist 文案更新
    tts_pat = re.compile(r'("sectionId"\s*:\s*"interactive-model"[\s\S]{0,200}?"text"\s*:\s*")([^"]*)(")')
    def fix_tts(m):
        return m.group(1) + f"现在做互动实验：{cfg['title']}。{cfg['task']}" + m.group(3)
    html = tts_pat.sub(fix_tts, html)

    if not DRY:
        p.write_text(html, encoding="utf-8")
    return cid, "、".join(actions), True


def main():
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    ok = skip = fail = 0
    for cid in sorted(CONFIGS):
        if only and cid not in only:
            continue
        if not (COMMUNITY / cid / "index.html").is_file():
            print(f"❌ {cid}: 无 index.html"); fail += 1; continue
        try:
            cid2, msg, changed = process(cid)
            if changed:
                ok += 1
                print(f"{'[DRY] ' if DRY else ''}✅ {cid2}: {msg}")
            else:
                skip += 1
                print(f"⏭️  {cid2}: {msg}")
        except Exception as e:
            fail += 1
            print(f"❌ {cid}: {type(e).__name__} {e}")
    print(f"\n替换 {ok}，跳过 {skip}，失败 {fail}{'（dry-run）' if DRY else ''}")


if __name__ == "__main__":
    main()
