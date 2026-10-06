#!/usr/bin/env python3
"""Add topic-specific depth modules to math-e (小学数学 shell) courses.

Elementary math-e shells often pass via template sections but lack
topic-specific core teaching. Each course gets 知识精讲 + 方法范例 with a
worked example, a 常见误区 note and TWO diagnostics: one concept
discrimination item and one calculation/application item. No mp4.
Idempotent via id="lesson-focus". Unique CSS/JS ids: mathe-depth-*.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-20"


def Q(question, options, correct, feedback):
    return dict(question=question, options=options, correct=correct, feedback=feedback)


def C(ct, cb, mt, mb, ex, pit, quizzes):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, pitfall=pit, quizzes=quizzes,
    )


COURSES = {
    "math-e-area-rectangle": C(
        "长方形与正方形的面积",
        "面积表示物体表面或封闭图形的大小。常用面积单位有平方厘米、平方分米、平方米。长方形面积=长×宽，正方形面积=边长×边长。求面积前要先统一长度单位，结果要用面积单位。周长是围一圈的长度，面积是铺满内部的大小，二者不要混淆。",
        "方法：统一单位 → 套公式 → 验算单位",
        "先确认是长方形还是正方形，量出需要的边长并统一单位，再代入公式。组合图形可分割成几个长方形分别求再相加，或用大长方形减去缺角部分。",
        "长 8 厘米、宽 5 厘米的长方形，面积=8×5=40 平方厘米；边长 6 厘米的正方形，面积=6×6=36 平方厘米。",
        "常见误区是把面积公式和周长公式搞混，或长度单位不统一就相乘。",
        [
            Q("长方形面积的计算公式是？",
              ["长+宽", "长×宽", "(长+宽)×2", "长×长"],
              1, "长方形面积=长×宽；(长+宽)×2 是周长。"),
            Q("一个长方形长 9 厘米、宽 4 厘米，面积是？",
              ["13 平方厘米", "26 平方厘米", "36 平方厘米", "72 平方厘米"],
              2, "9×4=36 平方厘米。"),
        ],
    ),
    "math-e-average-concept": C(
        "平均数的意义",
        "平均数表示一组数据的“一般水平”或“典型水平”，不是某一个真实数据，而是用“总数÷个数”得到的代表值。它能帮助我们比较几组数据整体谁高谁低，也能估计总量。平均数会受到极端大数或小数的影响。",
        "方法：先求和，再除以个数",
        "求平均数：把所有数据加起来得到总和，再除以数据的个数。比较两组数据时，先分别求平均数再比较。估算时可用“移多补少”想象：把多的部分补给少的，使大家一样多。",
        "小明三天读书页数是 12、18、15，平均数=(12+18+15)÷3=45÷3=15 页。",
        "常见误区是以为平均数一定等于某一个原始数据，或求和后忘记除以个数。",
        [
            Q("平均数表示的是？",
              ["最大的那个数", "一组数据的一般水平", "一定等于某个原始数据", "数据的个数"],
              1, "平均数反映一组数据的一般（典型）水平。"),
            Q("4、6、8、10 四个数的平均数是？",
              ["6", "7", "8", "28"],
              1, "(4+6+8+10)÷4=28÷4=7。"),
        ],
    ),
    "math-e-circle-perimeter-area": C(
        "圆的周长与面积",
        "圆是到定点（圆心）距离等于定长（半径）的所有点组成的图形。直径是半径的 2 倍。圆的周长 C=πd=2πr，表示圆一周的长度；圆的面积 S=πr²，表示圆面的大小。π 约取 3.14。求周长或面积前先分清给的是半径还是直径。",
        "方法：先判 r 还是 d，再选公式",
        "题目给直径先写成 r=d÷2（求面积时），或直接用 C=πd（求周长）。求面积必须用半径：S=πr²。计算后检查单位：周长用长度单位，面积用面积单位。",
        "半径 3 厘米的圆：周长≈2×3.14×3=18.84 厘米；面积≈3.14×3²=28.26 平方厘米。",
        "常见误区是求面积时误用直径直接代入 πr²，或把周长单位写成平方单位。",
        [
            Q("圆的面积公式是？",
              ["πd", "2πr", "πr²", "πr"],
              2, "圆面积 S=πr²；πd 与 2πr 是周长公式。"),
            Q("直径 10 厘米的圆，半径是？周长约是？（π取3.14）",
              ["半径5厘米，周长约31.4厘米", "半径10厘米，周长约31.4厘米", "半径5厘米，周长约15.7厘米", "半径10厘米，周长约62.8厘米"],
              0, "r=d÷2=5；C=πd≈3.14×10=31.4 厘米。"),
        ],
    ),
    "math-e-division-concept": C(
        "除法的初步认识",
        "除法表示“平均分”或“包含除”：把总数平均分成几份，求每份是多少；或看总数里包含几个同样大的数。除法算式 a÷b=c 中，a 是被除数，b 是除数，c 是商。除法是乘法的逆运算：若 a÷b=c，则 b×c=a（b≠0）。",
        "方法：想乘法，验除法",
        "遇到除法，先想“几乘几等于被除数”。平均分问题抓住“总数、份数、每份数”；包含除抓住“总数里有几个同样多”。用乘法验算：除数×商是否等于被除数。",
        "把 12 个苹果平均分给 3 人，每人几个？12÷3=4，因为 3×4=12。",
        "常见误区是把“平均分给几人”和“每人分几个”问法混淆，导致除数与商颠倒。",
        [
            Q("12÷3=4 可以用哪道乘法来验算？",
              ["12×3=36", "3×4=12", "12×4=48", "4÷3=12"],
              1, "除数×商=被除数，即 3×4=12。"),
            Q("把 15 支铅笔平均分给 5 人，每人几支？",
              ["3", "5", "10", "20"],
              0, "15÷5=3，因为 5×3=15。"),
        ],
    ),
    "math-e-measurement-sense": C(
        "量感：选择合适的计量单位",
        "量感是对长度、质量、时间、面积等量的大小的直觉判断。学习计量时，不仅要会换算，更要能根据生活经验选择合适的单位：身高用米或厘米，书本厚度用毫米，一袋米用千克，一堂课用分钟等。估计时先找参照物，再比较。",
        "方法：想参照物 → 选单位 → 估一估",
        "估计长度可想：一拃大约几厘米、一步大约几分米、教室门大约高两米。估计质量可想：一个苹果大约 200 克、一瓶水大约 500 毫升。先选对单位，再估数值范围。",
        "一支铅笔长约 18 厘米（不是 18 米）；一袋盐约 500 克（不是 500 千克）。",
        "常见误区是单位选错（把人的身高说成 160 米），或只会换算不会结合生活经验估计。",
        [
            Q("测量教室的长度，较合适的单位是？",
              ["毫米", "米", "千米", "吨"],
              1, "教室长度通常用米来计量。"),
            Q("一个西瓜大约重 5（  ），括号里最合适的是？",
              ["克", "千克", "吨", "厘米"],
              1, "一个西瓜大约几千克，用千克合适。"),
        ],
    ),
    "math-e-median-mode": C(
        "中位数与众数",
        "中位数是把一组数据按大小排列后，最中间的那个数（个数为偶数时取中间两个数的平均数），它不易受极端值影响。众数是出现次数最多的数，一组数据可以有一个众数、多个众数，也可能没有众数。平均数、中位数、众数从不同角度描述数据特征。",
        "方法：先排序找中位，再数次数找众数",
        "求中位数：从小到大（或从大到小）排好，找正中间。求众数：统计每个数出现几次，次数最多的就是众数。分析“谁更能代表”时，看是否有极端值、是否关心出现最多的情况。",
        "数据 2、5、5、7、9：中位数是 5；众数也是 5（出现两次）。",
        "常见误区是不排序就取中间位置的数，或把平均数误当成众数。",
        [
            Q("求中位数时，首先要做的是？",
              ["直接取第一个数", "把数据按大小排序", "只看最大数", "把所有数相加"],
              1, "必须先按大小排序，再找最中间的数。"),
            Q("数据 3、4、4、6、8 的众数是？",
              ["3", "4", "6", "8"],
              1, "4 出现了两次，次数最多，是众数。"),
        ],
    ),
    "math-e-mixed-operations": C(
        "混合运算的运算顺序",
        "同级运算（只有加减，或只有乘除）要从左到右依次计算。既有加减又有乘除时，要先算乘除，再算加减。有括号时，先算括号里面的。正确的运算顺序是算对混合运算的关键。",
        "方法：看符号定顺序，有括号先去括号",
        "计算前先用笔标出先算哪一步：有括号圈出括号内；没有括号则先标乘除。一步一步写脱式，等号对齐，避免跳步出错。",
        "计算 3+4×5：先算 4×5=20，再算 3+20=23。计算 (3+4)×5：先算括号 7，再 7×5=35。",
        "常见误区是一律从左到右算，忽略“先乘除后加减”，或漏算括号。",
        [
            Q("计算 6+8÷2，正确的第一步是？",
              ["先算 6+8", "先算 8÷2", "先算 6÷2", "三个数随便算"],
              1, "有加减又有乘除，先算除法 8÷2。"),
            Q("3+4×5 的结果是？",
              ["35", "23", "27", "12"],
              1, "先 4×5=20，再 3+20=23。"),
        ],
    ),
    "math-e-multi-digit-addition-subtraction": C(
        "多位数加减法",
        "多位数加减要数位对齐，从个位算起。加法：某一位满十向前一位进 1。减法：某一位不够减，向前一位借 1 当 10。相同数位上的数才能相加减。算完可用估算或逆运算验算，养成检验习惯。",
        "方法：对齐数位 → 逐位计算 → 处理进退位",
        "列竖式时个位对个位、十位对十位。加法满十进一；减法不够减就借一当十，并记住被借的那一位要减 1。可用“加验减、减验加”检查。",
        "计算 386+257：个位 6+7=13，写 3 进 1；十位 8+5+1=14，写 4 进 1；百位 3+2+1=6，得 643。",
        "常见误区是数位没对齐，或进位、退位时漏加漏减。",
        [
            Q("列竖式计算多位数加法，首先要做到？",
              ["从高位算起", "相同数位对齐", "只对齐个位", "不必对齐"],
              1, "相同数位对齐后，再从个位算起。"),
            Q("523−178，个位计算时应？",
              ["直接 3−8", "从十位借 1，用 13−8", "个位结果写 0", "改成 8−3"],
              1, "个位不够减，向前借 1 当 10，用 13−8=5。"),
        ],
    ),
    "math-e-operations-laws": C(
        "运算律：让计算更简便",
        "加法交换律：a+b=b+a；加法结合律：(a+b)+c=a+(b+c)。乘法交换律：a×b=b×a；乘法结合律：(a×b)×c=a×(b×c)；乘法分配律：a×(b+c)=a×b+a×c。运算律可以帮助我们改变运算顺序或拆分数字，使口算、笔算更简便。",
        "方法：凑整、拆分、提公因数",
        "看到能凑整的数（如 25 与 4、125 与 8），优先用交换律、结合律调整顺序。看到乘一个和（或差），想分配律展开或反过来提取公因数合并。",
        "计算 25×16×4：先 25×4=100，再 100×16=1600。计算 35×102=35×(100+2)=3500+70=3570。",
        "常见误区是乱用分配律（如把 a+(b×c) 拆成 a+b 与 a+c），或凑整时漏掉某个因数。",
        [
            Q("下列属于乘法分配律的是？",
              ["a+b=b+a", "a×(b+c)=a×b+a×c", "(a×b)×c=a×(b×c)", "a×b=b×a"],
              1, "a×(b+c)=a×b+a×c 是乘法分配律。"),
            Q("用简便方法算 25×24，较好的一步是？",
              ["25×20+25×4", "25+24", "24÷25", "只算 25×20"],
              0, "24=20+4，用分配律：25×20+25×4=500+100=600。"),
        ],
    ),
    "math-e-percentage": C(
        "百分数的意义",
        "百分数表示一个数是另一个数的百分之几，也叫百分率或百分比，用“%”表示。把标准量看作 100 份，比较量占其中多少份，就是百分之几。百分数后面通常不带单位，它表示的是两个数量的倍比关系，常用于及格率、出勤率、折扣等。",
        "方法：找准单位“1”，再化成百分数",
        "先明确“谁是谁的百分之几”：把被比较的量÷标准量，再乘 100%，写成百分数。分数、小数、百分数可以互化：0.25=25/100=25%。",
        "一本书 200 页，已读 50 页，已读页数占全书的 50÷200=0.25=25%。",
        "常见误区是分不清谁是单位“1”，或把百分数当成带单位的具体数量。",
        [
            Q("百分数表示的是？",
              ["一个具体的长度", "一个数是另一个数的百分之几", "只能表示大于 1 的数", "只能用于钱"],
              1, "百分数表示两个数量的倍比关系。"),
            Q("40 是 200 的百分之几？",
              ["5%", "20%", "40%", "200%"],
              1, "40÷200=0.2=20%。"),
        ],
    ),
    "math-e-percentage-statistics": C(
        "百分数与统计",
        "统计中常用百分数描述各类数量占总体的比例，如及格率、出勤率、市场占有率。扇形统计图用扇形大小表示各部分占总体的百分之几，各部分百分数之和应为 100%。读图时先看总体是多少，再用百分比求具体数量。",
        "方法：读总体 → 读百分比 → 求数量或作比较",
        "从统计图或表格中先确认总数，再读某类所占百分数，用“总数×百分数”求该类数量；比较谁多谁少可直接比百分数（总体相同的时候）。",
        "全班 40 人，喜欢足球的占 25%，喜欢足球的有 40×25%=10 人。",
        "常见误区是直接把百分数当作人数，或各部分百分数相加不等于 100% 却不检查。",
        [
            Q("扇形统计图中各部分百分数之和通常是？",
              ["50%", "100%", "200%", "不一定"],
              1, "各部分合起来是总体，百分数之和为 100%。"),
            Q("某班 50 人，及格率为 80%，及格人数是？",
              ["8 人", "16 人", "40 人", "80 人"],
              2, "50×80%=40 人。"),
        ],
    ),
    "math-e-position-direction": C(
        "位置与方向",
        "在平面图上，常用东、南、西、北四个基本方向，以及东北、东南、西南、西北等来描述物体的位置关系。确定方向一般先找“北”，再辨认其他方向。描述位置还要说明“以谁为观察点”以及距离远近，这样才能说清楚。",
        "方法：先定北，再定观察点，最后说方向与距离",
        "读地图先找到指向标或“上北下南、左西右东”。说“A 在 B 的什么方向”时，以 B 为观察点看 A。结合格子图可数格表示大概距离。",
        "学校在公园的东面 200 米，意思是：站在公园看，学校在东方，距离约 200 米。",
        "常见误区是弄反观察点（把“A 在 B 的东面”说成“B 在 A 的东面”），或没先确定北方。",
        [
            Q("描述“图书馆在超市的北面”，观察点是？",
              ["图书馆", "超市", "任意地点", "东方"],
              1, "以超市为观察点，看图书馆在北面。"),
            Q("面向北方时，右手方向大致是？",
              ["东", "南", "西", "北"],
              0, "面北时，右手为东，左手为西。"),
        ],
    ),
    "math-e-possibility-concept": C(
        "可能性的初步认识",
        "生活中有些事一定会发生（必然），有些事一定不会发生（不可能），有些事可能发生也可能不发生（可能）。用“一定”“不可能”“可能”描述事件的可能性，是概率学习的起点。判断时要依据规则和条件，而不是主观愿望。",
        "方法：先看规则，再判断一定 / 可能 / 不可能",
        "摸球、掷骰子、转盘等问题：先明确袋子里有什么、骰子有几面、转盘分区是否均匀。若结果只有一种可能就是“一定”；完全没有对应结果就是“不可能”；有的有、有的没有就是“可能”。",
        "袋中只有红球：摸出红球是一定的，摸出蓝球是不可能的。袋中有红有蓝：摸出红球是可能的。",
        "常见误区是凭“我觉得”判断可能性，或把“可能”说成“一定”。",
        [
            Q("掷一枚普通骰子，点数是 7，这件事是？",
              ["一定发生", "可能发生", "不可能发生", "偶尔一定发生"],
              2, "普通骰子只有 1～6 点，不可能出现 7。"),
            Q("袋中有 3 个红球和 2 个黄球，摸出一个球是红球，这件事是？",
              ["一定", "不可能", "可能", "无法判断"],
              2, "有红球也有黄球，摸到红球是可能发生的。"),
        ],
    ),
    "math-e-solid-surface-area": C(
        "长方体和正方体的表面积",
        "表面积是立体图形所有外表面的面积之和。长方体有 6 个面：通常相对的面面积相等，表面积=2×(长×宽+长×高+宽×高)。正方体 6 个面都是相同的正方形，表面积=6×棱长×棱长。求表面积前先分清棱长数据，并统一单位。",
        "方法：先求每个面，再相加（或用公式）",
        "可以画出长方体展开图，分别算出前面、上面、侧面再乘 2 相加；也可以直接套公式。若是无盖纸盒，要记得减去盖子那一个面的面积。",
        "长 5 厘米、宽 3 厘米、高 2 厘米的长方体，表面积=2×(5×3+5×2+3×2)=2×(15+10+6)=62 平方厘米。",
        "常见误区是只算了 3 个面忘乘 2，或把体积公式当成表面积。",
        [
            Q("正方体表面积公式是？",
              ["棱长×棱长×棱长", "6×棱长×棱长", "4×棱长", "2×(长×宽)"],
              1, "正方体 6 个面相同，表面积=6×棱长²。"),
            Q("棱长 4 厘米的正方体，表面积是？",
              ["16 平方厘米", "64 平方厘米", "96 平方厘米", "24 平方厘米"],
              2, "6×4×4=96 平方厘米。"),
        ],
    ),
    "math-e-symmetry-translation-rotation": C(
        "对称、平移与旋转",
        "轴对称图形沿一条直线对折后，直线两旁的部分能够完全重合，这条直线叫对称轴。平移是图形沿直线方向移动，形状、大小、方向不变，只改变位置。旋转是图形绕一个点转动，形状、大小不变，位置和方向改变。三者都是常见的图形变换。",
        "方法：看“变了什么、没变什么”",
        "判断变换：重合对折→轴对称；沿直线滑动且方向不变→平移；绕点转动→旋转。画对称图形时，对应点到对称轴距离相等；画平移时，对应点移动方向和距离相同。",
        "国旗上的五角星是轴对称图形；电梯轿厢上升是平移；时钟指针走动是旋转。",
        "常见误区是把平移后方向改变的情况当成平移，或画轴对称时对应点距离不相等。",
        [
            Q("沿一条直线对折后两部分完全重合的图形叫做？",
              ["旋转图形", "轴对称图形", "放大图形", "平移图形"],
              1, "对折能完全重合的是轴对称图形。"),
            Q("下列现象属于平移的是？",
              ["风扇叶片转动", "拉抽屉", "钟摆左右摆动", "地球自转"],
              1, "拉抽屉是沿直线移动，形状方向不变，属于平移。"),
        ],
    ),
    "math-e-triangle-properties": C(
        "三角形的认识与特性",
        "三角形由三条线段首尾相连围成，有三条边、三个角、三个顶点。按角可分为锐角三角形、直角三角形、钝角三角形；按边可分为等腰三角形、等边三角形等。三角形具有稳定性：三角形的三条边长度确定后，形状就固定了，不易变形。",
        "方法：先看角分类，再看边分类；应用想稳定性",
        "判断三角形类型：有一个直角就是直角三角形；有一个钝角就是钝角三角形；三个角都是锐角就是锐角三角形。生活中脚手架、自行车三角架利用的就是三角形稳定性。",
        "三角板中有一个角是 90°，所以它是直角三角形；电线杆上的斜支架做成三角形，是为了稳固。",
        "常见误区是以为三角形会像四边形那样容易拉动变形，或分类时只看边不看角。",
        [
            Q("三角形最重要的特性是？",
              ["不稳定性", "稳定性", "可以任意变形", "只有两个角"],
              1, "三角形具有稳定性，边长确定后形状固定。"),
            Q("有一个角是钝角的三角形叫做？",
              ["锐角三角形", "直角三角形", "钝角三角形", "等边三角形"],
              2, "有一个钝角的是钝角三角形。"),
        ],
    ),
}


STYLE = """
<style id="mathe-depth-css">
.mathe-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.mathe-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.mathe-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.mathe-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.mathe-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.mathe-depth .mathe-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.mathe-depth .mathe-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="mathe-depth-js">
function matheDepthCheck(button, isCorrect, feedbackId, explanation) {
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


def build_check(quiz: dict, index: int, label: str) -> str:
    feedback_id = f"mathe-depth-feedback-{index}"
    options = []
    for idx, opt in enumerate(quiz["options"]):
        correct = idx == quiz["correct"]
        handler = "matheDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false",
            f=feedback_id,
            e=json.dumps(quiz["feedback"], ensure_ascii=False),
        )
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0",
                h=html.escape(handler, quote=True),
                letter=chr(65 + idx),
                opt=html.escape(opt),
            )
        )
    return f"""      <div class="module-check" data-conceptest="true">
        <h3>{html.escape(label)}</h3>
        <p>{html.escape(quiz['question'])}</p>
        {''.join(options)}
        <div class="mathe-feedback" id="{feedback_id}" role="status"></div>
      </div>
"""


def build_block(cfg: dict) -> str:
    labels = ["马上练 1：概念辨析", "马上练 2：计算应用"]
    checks = "".join(
        build_check(quiz, i + 1, labels[i] if i < len(labels) else f"马上练 {i + 1}")
        for i, quiz in enumerate(cfg["quizzes"])
    )
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section mathe-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section mathe-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="mathe-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
{checks}    </div>
  </section>
</section>
"""


def find_insert_at(source: str) -> int:
    dpos = -1
    for anchor in ('id="deep-understanding"', 'id="transfer-task"', 'id="posttest"', 'id="summary"'):
        dpos = source.find(anchor)
        if dpos >= 0:
            break
    if dpos < 0:
        return -1
    # Prefer slide-page boundary when present (deck courses).
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    if marker >= 0:
        return marker
    # Shell pages: insert immediately before the tag that owns the anchor id.
    tag_start = source.rfind("<", 0, dpos)
    if tag_start >= 0:
        return tag_start
    return source.rfind("<section", 0, dpos)


def upgrade(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="lesson-focus"' in source:
        return False, "already upgraded"
    insert_at = find_insert_at(source)
    if insert_at < 0:
        return False, "insert anchor not found"
    source = source[:insert_at] + build_block(cfg) + "\n" + source[insert_at:]
    if 'id="mathe-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="mathe-depth-js"' not in source:
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
    return True, f"2 depth modules + {len(cfg['quizzes'])} checks"


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
