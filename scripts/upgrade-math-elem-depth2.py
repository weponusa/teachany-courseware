#!/usr/bin/env python3
"""Add depth modules + a canvas visualization to remaining math-elem courses.

Batch 2: all math-elem courses still lacking id="lesson-focus" (37 courses).
Reuses STYLE / CHECK_SCRIPT / build_block / upgrade / main from
upgrade-math-elem-depth.py (CSS/JS ids identical). Extends canvas kinds with
pie / bars / circle / shapes where existing kinds are not close enough.
Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-20"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit, kind, viz_title, viz_desc):
    return dict(concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
                example=ex, question=q, options=opts, correct=correct, feedback=fb,
                pitfall=pit, kind=kind, viz_title=viz_title, viz_desc=viz_desc)


COURSES = {
    "math-elem-area-units": C(
        "面积单位：从平方厘米到公顷", "面积单位表示图形或物体表面的大小。常用单位有平方厘米（cm²）、平方分米（dm²）、平方米（m²），较大的还有公顷（hm²）和平方千米（km²）。相邻常用单位间：1平方分米=100平方厘米，1平方米=100平方分米，1公顷=10000平方米。选单位要看物体大小，如邮票用平方厘米、教室地面用平方米。",
        "方法：先估大小再选单位", "先想象物体有多大，再选合适的面积单位；需要换算时按“百进”关系：相邻单位之间一般是100倍（公顷到平方米是10000倍）。做题时先统一单位再比较或计算，结果要带上面积单位。",
        "一张课桌面大约是50平方分米；篮球场大约是400多平方米；一个足球场大约是0.7公顷。把3平方分米换成平方厘米：3×100=300平方厘米。",
        "教室地面面积比较合适的单位是？", ["平方厘米", "平方米", "平方千米", "公顷"], 1,
        "教室地面一般几十平方米，用平方米最合适。",
        "常见误区是把长度单位当成面积单位（如用“米”说面积），或换算时忘了相邻单位是100倍而按10倍算。应记住面积单位带“平方”，相邻常用单位多为百进。",
        "grid", "面积单位与方格", "每个小方格若表示1平方厘米，数出格子数就能体会面积单位的大小。"),
    "math-elem-average-median": C(
        "平均数与中位数", "平均数是一组数据的总和除以个数，反映这组数据的“一般水平”。中位数是把数据按大小排列后最中间的那个数（个数为偶数时取中间两数的平均数），它不受极端大数或小数的影响太大。生活中成绩、气温等常用平均数，收入分布等有时更适合看中位数。",
        "方法：先排序再求，或先求和再除", "求平均数：先把所有数据加起来，再除以数据的个数。求中位数：先把数据从小到大（或从大到小）排好，找出最中间的一个；若有偶数个，取中间两个的平均数。解题前先弄清题目要的是平均数还是中位数。",
        "数据 2、5、7、8、13：平均数=(2+5+7+8+13)÷5=7；中位数是排序后的中间数7。数据 3、4、6、10：中位数=(4+6)÷2=5。",
        "求平均数正确的步骤是？", ["只看最大数", "总和除以个数", "只取中间数", "最大减最小"], 1,
        "平均数=所有数据的总和÷数据的个数。",
        "常见误区是把中位数当成平均数，或求中位数前没有先排序。应分清：平均数要“求和再除”，中位数要“先排序找中间”。",
        "linechart", "数据与平均水平", "折线上各点表示数据，水平趋势可对照平均数，帮助理解“一般水平”。"),
    "math-elem-circle-area": C(
        "圆的面积", "圆的面积是圆所围成平面的大小。圆的面积公式是 S=πr²，其中 r 是半径；若已知直径 d，则 r=d÷2，再代入公式。π 常用 3.14。求面积前要认清给的是半径还是直径，单位统一后再计算，结果用面积单位。",
        "方法：先找半径再套公式", "读题先确定半径：给直径就除以2，给周长可先求半径（C=2πr）。再计算 r²，最后乘 π。组合图形可把圆与正方形等分开算再相加或相减。验算时估一估：圆面积大约是“半径的平方”的3倍多。",
        "半径3厘米的圆，面积≈3.14×3×3=28.26平方厘米；直径8厘米则半径4厘米，面积≈3.14×16=50.24平方厘米。",
        "圆的面积公式是？", ["πr", "2πr", "πr²", "πd"], 2,
        "圆面积 S=πr²；2πr 是周长。",
        "常见误区是用直径直接代入 πr²，或把周长公式和面积公式搞混。应先化成半径，牢记面积是 πr²、周长是 2πr。",
        "circle", "圆的面积示意", "半径为 r 的圆，面积等于 π 个边长为 r 的正方形的面积，即 S=πr²。"),
    "math-elem-complex-word-problems": C(
        "稍复杂的应用题：分步与综合", "稍复杂的应用题往往包含两步或更多运算，要把生活情境翻译成数学关系。常见类型有：先求中间量再求结果、已知总量和部分求另一部分、以及需要“假设—检验”的问题。关键是读懂题意，弄清已知什么、求什么、中间还缺什么。",
        "方法：画图列式、分步求解", "先圈出关键词和数量，用线段图或关系式理清数量关系；能分步的先算出中间结果，再代入下一步。算完用估算或代入原题检验是否合理。遇到多余条件要会筛选，不要被无关数字迷惑。",
        "一本书120页，小明第一天看了全书的1/4，第二天看了剩下的1/3，第二天看了多少页？先求第一天：120×1/4=30页，剩下90页；第二天：90×1/3=30页。",
        "解稍复杂应用题时，最重要的第一步是？", ["直接乘加减", "弄清已知、所求和中间量", "只看最后一个数", "随便列式"], 1,
        "先理清已知、所求和需要的中间量，再分步列式。",
        "常见误区是看到数字就急着运算，不分析数量关系，或漏掉中间步骤。应先读题画图，分清直接条件和间接条件，再分步计算并验算。",
        "numberline", "线段图理清关系", "用数轴（线段图）标出总量和各部分，复杂问题也能一步步看清。"),
    "math-elem-decimal-operations": C(
        "小数的加减乘除", "小数加减法要小数点对齐（即相同数位对齐），从低位算起，满十进一、不够减退位。小数乘法先按整数乘法算，再看两个因数一共有几位小数，积就保留几位小数。小数除法可转化为除数是整数的除法，商的小数点与被除数对齐。",
        "方法：对齐数位、定好小数点", "加减：竖式小数点对齐再算。乘法：先当整数乘，再从右往左数出小数位数点上小数点。除法：除数有小数时，除数和被除数的小数点同时右移相同位数，使除数变成整数再除。算完估算检验数量级是否合理。",
        "3.6+2.45：小数点对齐得6.05。1.2×0.3：12×3=36，共2位小数，积是0.36。4.8÷1.2：化为48÷12=4。",
        "小数加减竖式最关键的是？", ["小数点对齐", "末尾对齐", "位数一样多", "从左往右算"], 0,
        "小数加减必须小数点对齐，也就是相同数位对齐。",
        "常见误区是加减时末尾对齐导致错位，乘法积的小数位数数错，除法移动小数点时被除数和除数移动位数不一致。应牢记对齐数位、数清小数位数。",
        "numberline", "小数在数轴上", "数轴上能看清小数的大小与运算结果是否落在合理位置。"),
    "math-elem-division-intro": C(
        "除法的初步认识", "除法表示把一个数平均分成几份，或求一个数里有几个另一个数。如 12÷3=4，可读作“12除以3等于4”，表示把12平均分成3份，每份4；也可表示12里面有4个3。除法是乘法的逆运算：已知积和其中一个因数，求另一个因数。",
        "方法：平均分与包含分", "解决除法问题先分清是“平均分”（已知总数和份数，求每份多少）还是“包含分”（已知总数和每份多少，求能分几份）。可用实物或画图分一分，再用乘法验算：商×除数=被除数。",
        "有12颗糖，平均分给3个小朋友，每人得12÷3=4颗（平均分）；每袋装3颗，可装12÷3=4袋（包含分）。用4×3=12验算正确。",
        "12÷3=4 表示的意义可以是？", ["12加3", "把12平均分成3份，每份4", "12减3得4", "3个12"], 1,
        "12÷3=4 表示把12平均分成3份每份是4，或12里有4个3。",
        "常见误区是分不清“平均分”和“包含分”，或除法算式写反（被除数与除数颠倒）。应结合实物操作理解“分”，并用乘法验算。",
        "grid", "平均分示意图", "12个方格平均分成3行，每行4个，直观理解 12÷3=4。"),
    "math-elem-equation-intro": C(
        "方程的初步认识", "方程是含有未知数的等式，如 x+5=12。等号两边表示相等的两个量。解方程就是求出未知数是多少，使等式成立。天平平衡的道理可以帮助理解：一边变了，另一边也要做同样的变化才能保持相等。",
        "方法：利用等式性质求解", "解简易方程常用“移项”或“两边同时加减乘除同一个数（除数不为0）”：等号两边同时加上或减去同一个数，或同时乘除同一个不为0的数，等式仍成立。求出未知数后要代入原方程检验。",
        "解 x+7=15：两边同时减7，得 x=8；检验：8+7=15，正确。解 3x=18：两边同时除以3，得 x=6。",
        "下列式子中是方程的是？", ["3+5=8", "x+5=12", "7-2", "x+5"], 1,
        "方程必须是含有未知数的等式，x+5=12 符合。",
        "常见误区是把不含等号的式子或没有未知数的算式也叫方程，解方程时只变一边导致等式破坏。应记住方程=含未知数的等式，两边要同时变化。",
        "numberline", "未知数在数轴上", "在数轴上标出已知量和未知量的位置，帮助理解等式两边平衡。"),
    "math-elem-four-operations-laws": C(
        "四则运算定律", "加法有交换律（a+b=b+a）和结合律（(a+b)+c=a+(b+c)）；乘法有交换律、结合律和分配律 a×(b+c)=a×b+a×c。减法、除法一般没有交换律。灵活运用运算定律可以简算，如凑整、提取公因数，提高计算速度和正确率。",
        "方法：凑整与提取公因数", "看到能凑成整十、整百的加数，用交换律、结合律先凑整；乘法中有相同因数或能拆成和差的，用分配律展开或反过来提取公因数。先观察数字特点再决定用哪条定律，算完用估算检验。",
        "25×48+25×52=25×(48+52)=25×100=2500；计算 37+28+63，可先 37+63=100，再加28得128。",
        "下列属于乘法分配律的是？", ["a+b=b+a", "a×(b+c)=a×b+a×c", "(a×b)×c=a×(b×c)", "a-b=b-a"], 1,
        "乘法分配律：一个数乘两个数的和，等于分别相乘再相加。",
        "常见误区是把分配律写成 a×(b+c)=a×b+c，漏乘后面的数；或错误地给减法、除法套用交换律。应记清各定律的适用运算，分配时每一项都要乘。",
        "numberline", "运算与位置", "在数轴上体会加法和乘法“合成”与“拆分”，理解结合与分配的道理。"),
    "math-elem-fraction-decimal-percent": C(
        "分数、小数与百分数的互化", "分数、小数、百分数可以表示同一个量。小数化百分数：小数点向右移两位并加百分号，如0.35=35%。百分数化小数则相反。分数化小数用分子除以分母；能化成有限小数的分数，分母的质因数只有2和5。百分数表示一个数是另一个数的百分之几，分母是100。",
        "方法：抓住“百分之几”这座桥", "互化时以百分数或分母为100的分数为桥梁：小数↔百分数看小数点移动两位；分数↔百分数先化成小数或先通分到分母100。比较大小时可先化成同一种形式再比。",
        "3/4=0.75=75%；0.2=20%=1/5；18%=0.18=18/100=9/50。",
        "把0.45写成百分数是？", ["4.5%", "45%", "450%", "0.45%"], 1,
        "小数点向右移两位，0.45=45%。",
        "常见误区是小数点移动方向或位数搞错，以及认为百分数都小于1。应记住“移两位、加/去百分号”，并理解百分数可以大于100%。",
        "numberline", "同一点的三种表示", "数轴上同一个点可以用分数、小数、百分数表示，帮助建立互化观念。"),
    "math-elem-fraction-operations": C(
        "分数的加减乘除", "分数加减要先通分，分母相同后分子相加减，能约分的要约分。分数乘法：分子乘分子、分母乘分母，能约分可先约后乘。分数除法：除以一个数等于乘它的倒数，即 a/b÷c/d=a/b×d/c。计算前可先化带分数为假分数。",
        "方法：通分、约分、乘倒数", "加减：找公分母通分→分子加减→约分。乘法：能约分先约→上下分别相乘。除法：把÷改为×，后面分数上下颠倒成倒数再按乘法算。结果是假分数通常化成带分数或整数。",
        "1/2+1/3：通分为3/6+2/6=5/6。2/3×3/4：先约分得1/2×1/2=1/4。3/4÷1/2=3/4×2/1=3/2。",
        "分数除法的法则是？", ["分子分母直接相除", "除以一个数等于乘它的倒数", "只颠倒被除数", "通分后相减"], 1,
        "除以一个分数，等于乘这个分数的倒数。",
        "常见误区是加减时分子分母一起加减，除法时颠倒了被除数而不是除数。应牢记：加减先通分；除法颠倒除数再乘。",
        "grid", "分数运算示意图", "用方格表示几分之几的合并、拆分与倍分，理解通分和乘倒数。"),
    "math-elem-fractions-intro": C(
        "分数的初步认识", "把一个物体或一个整体平均分成若干份，表示其中一份或几份的数叫分数。如把一个饼平均分成4份，每份是1/4，读作“四分之一”；其中3份是3/4。分数线下面是分母，表示平均分成的份数；上面是分子，表示取出的份数。",
        "方法：平均分再数份数", "认识分数先确认“谁是单位1”，再看平均分成了几份（分母），取了几份（分子）。可用折纸、画图涂色来表示分数。比较分子是1的分数时，分母越大，每份反而越小。",
        "把一张纸对折再对折，平均分成4份，涂其中1份就是1/4，涂3份就是3/4。1/2 比 1/4 大，因为平均分的份数少，每份更大。",
        "分数 3/5 中的分母 5 表示？", ["取出3份", "平均分成5份", "一共有3个", "比5大"], 1,
        "分母表示把单位1平均分成的份数。",
        "常见误区是没有“平均分”就写成分数，或分子分母含义颠倒。应强调必须平均分，分母是份数、分子是取出的份数。",
        "grid", "涂色认识分数", "把长方形平均分成若干格并涂色，直观认识几分之几。"),
    "math-elem-fractions-meaning": C(
        "分数的意义", "分数可以表示把单位1平均分成若干份后取出的份数，也可以表示两个量之间的倍比关系。分数的基本性质：分数的分子和分母同时乘或除以同一个不为0的数，分数大小不变。据此可以进行约分和通分：约分得到最简分数，通分得到同分母分数以便比较或加减。",
        "方法：抓住基本性质约分通分", "约分：找分子分母的公约数，同时除到互质（只有公约数1）。通分：找分母的最小公倍数作公分母，分子作相应变化。比较异分母分数可先通分再比分子，或化成小数比较。",
        "2/4 约分得 1/2；比较 2/3 和 3/5：通分为 10/15 和 9/15，所以 2/3>3/5。3/6=1/2，分子分母同时除以3。",
        "分数基本性质是指分子分母同时？", ["加上同一个数", "乘或除以同一个不为0的数", "只乘分子", "随便变"], 1,
        "分子分母同时乘或除以同一个不为0的数，分数大小不变。",
        "常见误区是约分时只约分子或只约分母，通分时分子没有跟着变。应同时对分子分母做相同的乘除变化。",
        "numberline", "分数在数轴上", "同分母分数在数轴上从左到右依次增大，帮助理解分数的意义与大小。"),
    "math-elem-large-numbers": C(
        "大数的认识", "亿以内的数按四位一级：个级（个、十、百、千）、万级（万、十万、百万、千万）、亿级。读数时从高位读起，每级末尾的0不读，其他数位有一个或连续几个0都只读一个零。写数时对齐数级，哪一位上一个单位也没有就写0占位。",
        "方法：分级读、分级写", "读大数先从右向左四位分一级，标出“万”“亿”，再从高到低读出每级再加级名。写数先写最高级，再逐级写出，缺位补0。近似数可用四舍五入省略到万位或亿位等。",
        "10 304 000 读作一千零三十万四千；三千零五万零六十写作 30050060。45000 省略万位后面的尾数约为5万。",
        "读大数时，连续几个0通常？", ["每个0都读出来", "只读一个零", "都不读", "读成“十”"], 1,
        "其他数位上一个或连续几个0，一般只读一个零。",
        "常见误区是级数分错导致读错写错，或每级中间的0漏读、末尾的0却多读。应坚持四位一级，按级读写并注意0的读法。",
        "numberline", "大数的位置感", "在数轴上感受万、十万等数量级，建立大数的空间观念。"),
    "math-elem-length-units": C(
        "长度单位：毫米到千米", "常用长度单位有毫米（mm）、厘米（cm）、分米（dm）、米（m）、千米（km）。进率：10毫米=1厘米，10厘米=1分米，10分米=1米，1000米=1千米。测量较短物体用毫米、厘米，教室长度用米，路程用千米。选单位要符合生活经验。",
        "方法：估一估再量一量", "先估测物体大约多长，再选合适工具和单位测量；换算时看清相邻单位是10倍还是千米与米的1000倍。比较长度先统一单位。记住常用参照：指甲宽约1厘米，一步约半米到1米。",
        "一支铅笔长约18厘米=180毫米；4000米=4千米；3米5分米=35分米。操场跑道一圈常约400米。",
        "1米等于多少厘米？", ["10", "100", "1000", "10000"], 1,
        "1米=10分米=100厘米。",
        "常见误区是米与厘米、千米与米的进率记混，或估测时单位选得离谱。应熟记10进与1000米=1千米，并建立身体尺度作参照。",
        "numberline", "米尺上的长度", "数轴像一把米尺，刻度帮助理解毫米、厘米、分米的关系。"),
    "math-elem-mass-units": C(
        "质量单位：克、千克、吨", "质量表示物体所含物质的多少，常用单位有克（g）、千克（kg）、吨（t）。进率：1000克=1千克，1000千克=1吨。轻小物品用克，生活用品常用千克，很重的货物用吨。称重要选对秤和单位，估重要结合生活经验。",
        "方法：对照生活经验估重", "先估物体大约多重再选单位：一枚一元硬币约6克，一袋盐约500克，一个小学生体重几十千克，一辆卡车几吨。换算时按千进关系移动小数点或添减三个0。计算时先统一单位。",
        "2千克500克=2500克；3吨=3000千克；一瓶矿泉水约500克=0.5千克。",
        "1千克等于多少克？", ["10", "100", "1000", "10000"], 2,
        "1千克=1000克，1吨=1000千克。",
        "常见误区是把质量单位和长度单位混淆，或千克与克按100倍换算。应记住质量单位是克、千克、吨，相邻为千进。",
        "numberline", "质量的轻重感", "用数轴标记克与千克的位置，体会1000克就是1千克。"),
    "math-elem-multi-digit-divide": C(
        "多位数除法", "多位数除法按“试商→乘→减→落”循环进行：从被除数高位看起，够除就除，不够则多看一位；试商后用商乘除数，写在相应数位下，相减后落下一位再继续。除数是两位数时，可把除数看作整十数来试商，再根据余数调整。",
        "方法：试商要准，余数要小", "先估被除数前几位够不够除，确定商的位数；用整十估商，若余数大于或等于除数就改大商，若不够减就改小商。每一步余数必须小于除数。最后用“商×除数+余数=被除数”验算。",
        "计算 768÷24：24×3=72，76÷24商3余4，落下8得48，24×2=48，恰好除尽，商是32。验算：32×24=768。",
        "竖式除法中，每一步的余数必须？", ["大于除数", "小于除数", "等于被除数", "随便"], 1,
        "余数一定要小于除数，否则还可以再除。",
        "常见误区是试商偏大或偏小不调整，余数大于除数却继续往下算，或商的数位对错。应坚持估商、调整、验算三步。",
        "numberline", "除法与倍分", "在数轴上按除数一段段地量，理解“里面有几个”的除法意义。"),
    "math-elem-multi-digit-multiply": C(
        "多位数乘法", "多位数乘法用竖式：用乘数的每一位去乘另一乘数，注意数位对齐——用十位上的数去乘时，积的末位要写在十位上（相当于多一个0）。各部分积对齐相加得到积。乘法是求几个相同加数的和，也可用分配律把因数拆开简算。",
        "方法：逐位乘、对齐加", "从个位乘起，每一位乘完对准相应数位；有0时也要对准数位，不要漏零。可用估算先判断积大约是几位数、落在什么范围，算完再与估算对照。",
        "计算 36×24：36×4=144，36×20=720，144+720=864。也可 36×(20+4)=720+144=864。",
        "用十位上的数去乘时，积的末位应对准？", ["个位", "十位", "百位", "随便写"], 1,
        "用十位去乘，积的末位写在十位，相当于乘了10。",
        "常见误区是部分积没有错位，或中间有0时漏写。应牢记“用哪一位乘，末位就对哪一位”，并结合估算验算。",
        "grid", "乘法与阵列", "行列阵列直观表示“每行几个、有几行”，理解多位数乘法的意义。"),
    "math-elem-multiplication-table": C(
        "乘法口诀与表内乘法", "表内乘法是一位数乘一位数，结果可从乘法口诀中直接得出。口诀如“三六十二”表示3×6=18或6×3=18。乘法表示几个相同加数相加，也表示矩形阵列中的总数。熟练口诀是后续多位数乘除法的基础。",
        "方法：理解意义再记熟口诀", "先用实物或点子图理解“几乘几”，再通过对口诀、找规律（如5的口诀尾数是0或5）记熟。遗忘时可用加法或已知口诀推算，如记不住7×8，可用7×7=49再加7得56。",
        "4×7：口诀“四七二十八”，所以4×7=28。验证：4+4+4+4+4+4+4=28。正方形阵列边长6，点子总数6×6=36。",
        "口诀“五八四十”表示？", ["5+8=40", "5×8=40", "58=40", "5×4=8"], 1,
        "“五八四十”表示5×8=40（或8×5=40）。",
        "常见误区是只会背口诀不理解含义，或相近口诀混淆（如六七四十二与六八四十八）。应结合实物、阵列理解后再记忆，并经常练习。",
        "grid", "乘法阵列", "方格阵列中行数×每行格数=总数，对应一句乘法口诀。"),
    "math-elem-negative-numbers": C(
        "负数的初步认识", "正数是大于0的数，负数是小于0的数，0既不是正数也不是负数。温度低于0℃、海拔低于海平面、支出等常用负数表示。在数轴上，正数在0的右边，负数在0的左边，到0的距离叫绝对值。互为相反数的两个数到原点距离相等、方向相反。",
        "方法：借助生活情境与数轴", "先分清“零上/零下”“收入/支出”等相反意义的量，用正负号区分。在数轴上标出各数，比较大小：右边的数总比左边的大，如 -2>-5，-1<0。读题注意负号不要漏掉。",
        "零下3℃记作-3℃；比海平面低50米记作-50米。数轴上 -1 在 0 左边，1 在 0 右边，它们互为相反数。",
        "在数轴上，-3 和 -1 比较大小？", ["-3>-1", "-3<-1", "-3=-1", "无法比"], 1,
        "右边的数更大，-1 在 -3 右边，所以 -3<-1。",
        "常见误区是认为带负号的数一定更小却搞反（如以为-5>-2），或比较时只看数字忽略符号。应在数轴上比较，记住越往右越大。",
        "numberline", "正负数数轴", "0的左右两侧对称分布正负数，直观理解相反意义的量。"),
    "math-elem-number-recognition": C(
        "数的认识：读、写与组成", "认数要会读、会写、会说出组成。如23表示2个十和3个一；按数位从高到低读。认识计数单位“个、十、百……”以及相邻单位“满十进一”。通过实物、计数器、小棒把抽象的数和具体数量对应起来。",
        "方法：看数位说组成", "读写时先认清数位：从右往左个位、十位、百位……。说组成时按数位说“几个百、几个十、几个一”。比较大小从高位比起。数数时注意拐弯处（如29后面是30）。",
        "48里面有4个十和8个一；读写“一百零五”要注意中间的0占位，写作105。计数器上拨珠可表示这个数。",
        "35 的组成是？", ["3个一和5个十", "3个十和5个一", "35个十", "8个一"], 1,
        "35=3个十和5个一。",
        "常见误区是数位搞反、中间的0漏写，或数到拐弯处接错。应借助计数器强化数位，读写时注意0占位。",
        "numberline", "数的顺序", "数轴上从左到右数越来越大，帮助建立数序和大小观念。"),
    "math-elem-numbers-within-100": C(
        "100以内数的认识", "100以内的数由几个十和几个一组成，100是10个十。会数、会读、会写100以内各数，会比较大小，会完成整十数加减和接近整十的口算。认识数位：个位和十位，满十向十位进一。",
        "方法：整十突破与数轴定位", "先熟练整十数（10、20…100），再认识整十多几。比较大小先看十位，十位相同再看个位。在数轴或百数表上找到数的位置，体会相邻、大小和间隔。",
        "67=6个十和7个一；比较 58 和 63：十位5<6，所以58<63。从40数到50：41、42…49、50。",
        "比较 72 和 69，应先看？", ["个位", "十位", "相加", "相减"], 1,
        "先比较十位，7>6，所以72>69。",
        "常见误区是个位十位颠倒读写，比较大小只看个位。应强调十位是“几个十”，比较从高位起。",
        "numberline", "100以内数轴", "在0到100的数轴上定位，理解整十和几十几的位置关系。"),
    "math-elem-numbers-within-10000": C(
        "万以内数的认识", "万以内数有个、十、百、千、万等计数单位，10000是一万。读数从高位读起，中间有0要读零，末尾0不读；写数要对齐数位，缺位补0。会用四舍五入求近似数，如省略百位后面的尾数。",
        "方法：数位表对齐读写", "借助数位表，从高位到低位逐位读、写。说出一个数含有几个千、几个百等。比较大小从最高位比起。近似数看省略位的下一位是否满5决定四舍五入。",
        "3086读作三千零八十六；二千零五写作2005。4280省略百位后面的尾数约为4300。",
        "写“四千零三十”应写作？", ["430", "4030", "40030", "4300"], 1,
        "四千零三十是4030，十位是3，百位用0占位。",
        "常见误区是中间0漏写或多写，近似数四舍五入方向错误。应使用数位表占位，省略尾数时看下一位。",
        "numberline", "万以内的数级", "数轴分段标出千、百，感受万以内数的数量级。"),
    "math-elem-numbers-within-20": C(
        "20以内数的认识", "20以内数是后续计算的基础。11~20由1个十和几个一组成，20是2个十。要会按序数数、认读、书写，会比较大小，并初步理解“满十进一”。借助小棒、计数器把十和一分开看。",
        "方法：看成“十加几”", "把11~19都看成10加几，如14=10+4。比较大小可看离20或离10的远近，也可在数轴上比左右。写数字注意笔顺，区分6和9、12和21的数位。",
        "16里面有1个十和6个一；18比15大，因为个位8>5且十位相同。从1数到20要连续不跳数。",
        "14 可以看成？", ["1+4", "10+4", "40", "4个十"], 1,
        "14=1个十和4个一，即10+4。",
        "常见误区是把十几读成“十一几”或数位颠倒写成41。应强调“十和几”，并用小棒捆成一捆表示一个十。",
        "numberline", "20以内数轴", "0到20的数轴帮助认数、比大小和理解十加几。"),
    "math-elem-perimeter": C(
        "周长的认识与计算", "周长是封闭图形一周的长度。长方形周长=(长+宽)×2，或长×2+宽×2；正方形周长=边长×4。求周长要把各边长度加起来，注意单位统一。不规则图形可想象“拉直”成一条线来理解周长。",
        "方法：量边相加或套公式", "规则图形直接用公式；组合图形沿着外轮廓把外露的边长相加，公共边不重复加。先统一长度单位再算，结果是长度单位不是面积单位。",
        "长5厘米、宽3厘米的长方形，周长=(5+3)×2=16厘米；边长4厘米的正方形周长=4×4=16厘米。",
        "长方形周长公式是？", ["长×宽", "(长+宽)×2", "长+宽", "边长×边长"], 1,
        "长方形周长=(长+宽)×2；长×宽是面积。",
        "常见误区是把周长和面积公式混淆，或组合图形把中间的边也加进去。应分清周长是“一周边长之和”，只加外轮廓。",
        "grid", "周长绕一圈", "沿着长方形外框走一圈，边长之和就是周长。"),
    "math-elem-pictograph": C(
        "象形统计图", "象形统计图用小图标（如小星星、小人）表示数量，一个图标代表一定的单位数量。看图先看图例（一个图标代表几），再数图标个数并乘单位量，就能知道各类别的数量，还能比较多少、求相差或总和。",
        "方法：先看图例再计数", "读图步骤：读标题→看图例代表多少→数每类图标个数→个数×单位量=实际数量。比较时既可比图标多少，也可比算出的数量。制作时图标要整齐，图例要标明清楚。",
        "若一个★表示2人，某组画了5个★，则有10人；另一组3个★表示6人，两组相差4人。",
        "读象形统计图时，首先应弄清？", ["图画漂不漂亮", "一个图标代表多少", "只用眼睛估", "颜色含义"], 1,
        "必须先看图例，明确一个图标表示的数量单位。",
        "常见误区是忘记看图例，把一个图标当成1就直接数，导致数量算错。应养成“先看图例再计数”的习惯。",
        "bars", "象形图示意", "用色块高度模拟一排排图标，高度越高表示数量越多。"),
    "math-elem-pie-chart": C(
        "扇形统计图", "扇形统计图（饼图）用整个圆表示总量，各个扇形表示各部分占总量的百分之几。扇形圆心角越大、面积越大，该部分所占比例就越大。它适合表示部分与整体的关系，如兴趣小组人数占比、家庭开支构成等。",
        "方法：看比例不看绝对数", "读扇形图先看标题和各部分名称、百分数；比较哪部分最大看谁的扇形最大或百分数最高；若已知总量，部分量=总量×对应百分数。注意各部分百分数之和应为100%。",
        "全班40人，喜欢足球的占25%，则人数=40×25%=10人；若语文占30%、数学占25%，语文占比更大。",
        "扇形统计图最适合表示？", ["数量随时间变化", "部分占整体的百分比", "只能比多少个", "路线长短"], 1,
        "扇形图突出各部分占总体的比例关系。",
        "常见误区是把扇形大小直接当成具体人数而忽略总量，或百分数相加不等于100%却未察觉。应结合总量和百分数计算实际数量。",
        "pie", "扇形统计图", "整圆表示总体，各扇形表示各部分所占比例。"),
    "math-elem-plane-shapes": C(
        "平面图形的认识", "常见平面图形有长方形、正方形、三角形、圆、平行四边形、梯形等。它们都是平面上的封闭图形。长方形对边相等、四个角都是直角；正方形四边相等且四个角是直角；三角形有三条边三个角；圆是到定点距离等于定长的点的集合。认识图形要抓住边、角等特征。",
        "方法：看边数与角的特点", "辨认图形先数边、看角：有直角吗？对边平行或相等吗？四边是否都相等？圆没有角。生活中找一找门窗、书本、钟面、三角板等对应的图形，加深印象。",
        "课本封面近似长方形；手帕常是正方形；交通标志里有三角形和圆。正方形满足长方形的所有特征，是特殊的长方形。",
        "正方形一定是特殊的？", ["圆", "长方形", "三角形", "梯形"], 1,
        "正方形四角都是直角且对边相等，是特殊的长方形。",
        "常见误区是只看“像不像”而不抓特征，或认为正方形不是长方形。应依据边和角的本质特征判断。",
        "shapes", "常见平面图形", "对比长方形、正方形、三角形和圆的边与角特征。"),
    "math-elem-possibility": C(
        "可能性：一定、可能、不可能", "事件发生的可能性有大有小：一定会发生、可能会发生、不可能发生。摸球、掷硬币等活动中，某种情况的机会与“有利结果数”有关。定性描述用“一定、可能、不可能”；简单定量可用分数表示可能性大小，如抛一枚均匀硬币正面朝上的可能性是1/2。",
        "方法：先列全部可能再判断", "判断可能性时，先想清楚所有可能出现的结果是否机会均等，再看目标结果占多少。描述要用准确词语：没有机会用“不可能”，只有一种必然结果用“一定”，其余用“可能”，还可用“很大/很小”比较。",
        "袋中只有红球，摸出红球是一定；袋中有红有蓝，摸出红球是可能；袋中无绿球，摸出绿球不可能。硬币正面朝上可能性为1/2。",
        "袋中全是白球，摸出黑球是？", ["一定", "可能", "不可能", "各一半"], 2,
        "没有黑球，摸出黑球是不可能事件。",
        "常见误区是把“很难发生”说成“不可能”，或以为可能性大小与个人愿望有关。应依据实际条件客观判断。",
        "pie", "可能性示意", "用扇形大小表示不同结果所占机会，帮助比较可能性大小。"),
    "math-elem-ratio-proportion": C(
        "比和比例的初步认识", "比表示两个量的倍数关系，如2:3读作“2比3”，也可写成分数2/3。比的前项、后项同时乘或除以同一个不为0的数，比值不变。比例是表示两个比相等的式子，如2:3=4:6。解比例可用“两外项之积等于两内项之积”。",
        "方法：化简比与列比例", "化简比：前后项同除以公约数，化成最简整数比。求比值：前项除以后项。解决比例问题先找出相等的两个比，列成比例再解。注意比的后项不能为0。",
        "把10:15化简为2:3；比值=10÷15=2/3。若 a:3=4:6，则6a=12，a=2。",
        "比的基本性质是前后项同时？", ["加上同一个数", "乘或除以同一个不为0的数", "只变前项", "交换位置大小不变"], 1,
        "前后项同时乘或除以同一个不为0的数，比值不变。",
        "常见误区是化简比时只约一边，或把比的顺序写反导致意义改变。应同时变化前后项，并注意“谁比谁”的顺序。",
        "numberline", "比的分段", "把一条线段按比分成几段，直观理解比和比例。"),
    "math-elem-simple-equation": C(
        "解简易方程", "解方程是求出未知数的值使等式成立。简易方程常见类型：x±a=b、a±x=b、ax=b、x÷a=b 等。依据等式性质变形，最后把结果代入原方程检验。列方程解应用题时，先设未知数，再根据题中等量关系列方程。",
        "方法：同解变形并检验", "看未知数在哪一边、做了什么运算，用逆运算“还原”：加了就减、乘了就除。两边同时运算时，同一个数必须两边都变。解完代入检验，列方程题还要写答句。",
        "解 2x+3=11：两边减3得2x=8，两边除以2得x=4；检验2×4+3=11。设一支笔x元，3支共15元，则3x=15，x=5。",
        "解方程后必须做的步骤是？", ["再设一个未知数", "代入原方程检验", "擦掉题目", "只看商"], 1,
        "把求得的未知数代入原方程，检验等式是否成立。",
        "常见误区是移项变号错误，或检验时算错仍当对。应细心按等式性质变形，并养成检验习惯。",
        "numberline", "方程的平衡", "数轴上标出已知与未知，理解等式两边保持相等。"),
    "math-elem-solid-shapes": C(
        "立体图形的认识", "常见立体图形有长方体、正方体、圆柱、球、圆锥等。长方体有6个面、12条棱、8个顶点；正方体是特殊的长方体，六个面都是正方形。圆柱有两个圆形底面和一个曲面侧面；球是圆圆的、没有棱角。从不同方向观察会看到不同的面。",
        "方法：数面、棱、顶点并辨曲面", "辨认时看有没有曲面、各个面是什么形状、棱是否都相等。动手摸一摸、滚一滚：球能向各方向滚，圆柱能沿侧面滚动。找出生活中的纸箱、骰子、易拉罐、皮球等对应立体图形。",
        "鞋盒近似长方体；魔方是正方体；易拉罐近似圆柱；乒乓球是球。正方体棱长都相等，有12条棱。",
        "正方体有几条棱？", ["6", "8", "12", "4"], 2,
        "正方体有12条棱、6个面、8个顶点。",
        "常见误区是把圆柱和圆锥混淆，或数棱时漏数看不见的棱。应结合实物从多角度观察，并记住常见立体的面棱顶点数量。",
        "solid", "立体图形对比", "观察圆柱等立体的轮廓，建立空间观念。"),
    "math-elem-time-units": C(
        "时间单位：时、分、秒", "常用时间单位有时、分、秒。进率：60秒=1分，60分=1时，24时=1日。钟面上时针走一大格是1时，分针走一小格是1分，走一大格是5分。会认读整时、几时几分，会做简单的经过时间计算。",
        "方法：先认钟面再算经过时间", "读钟面：先看时针在两数之间确定几时，再看分针指的小格数（或大格×5）确定几分。求经过时间：结束时刻减开始时刻；跨小时注意借60分。生活中养成估时习惯，如一节课约40分。",
        "8时20分到9时05分经过45分；2时=120分；3分=180秒。分针从12走到4，经过20分。",
        "1小时等于多少分？", ["10", "24", "60", "100"], 2,
        "1时=60分，1分=60秒。",
        "常见误区是按十进制把1时当成100分，或读分针时把大格数错。应牢记60进率，读分针按小格或“大格×5”。",
        "numberline", "时间数轴", "把一日时间排在数轴上，理解时与分的先后和间隔。"),
    "math-elem-triangles-quadrilaterals": C(
        "三角形与四边形", "三角形由三条线段围成，按角可分为锐角三角形、直角三角形、钝角三角形；按边可分为等腰、等边、不等边三角形。三角形内角和是180°。四边形有四条边，常见有长方形、正方形、平行四边形、梯形。平行四边形对边平行且相等；梯形只有一组对边平行。",
        "方法：看角分类、看边分类", "辨认三角形先找有没有直角或钝角；辨认四边形看有几组平行边、角是不是直角、边是否相等。可用撕角拼接体验三角形内角和是180°。画图时用直尺、三角尺规范作图。",
        "有一个角是90°的三角形是直角三角形；长方形是四个角都是直角的特殊平行四边形。三角形三个角分别是40°、60°、80°，内角和180°。",
        "三角形的内角和是？", ["90°", "180°", "360°", "100°"], 1,
        "任意三角形三个内角之和都是180°。",
        "常见误区是仅凭“看起来尖”判断锐角钝角，或认为所有四边形都有两组对边平行。应依据定义用三角尺验证角和边的关系。",
        "shapes", "三角形与四边形", "对比不同三角形和四边形的边、角特征。"),
    "math-elem-volume-calculation": C(
        "体积的计算", "体积是物体所占空间的大小。长方体体积=长×宽×高，正方体体积=棱长×棱长×棱长。体积单位有立方厘米、立方分米、立方米等。求体积前统一长度单位，结果带体积单位。组合体可分割成几个长方体分别求再相加，或用大体积减去空缺。",
        "方法：量三边再相乘", "确认是长方体或正方体后，量出长、宽、高（或棱长），统一单位后相乘。若已知底面积和高，也可用体积=底面积×高。验算时估一估数量级是否合理。",
        "长4厘米、宽3厘米、高2厘米的长方体，体积=4×3×2=24立方厘米；棱长5厘米的正方体体积=125立方厘米。",
        "长方体体积公式是？", ["长×宽", "长×宽×高", "(长+宽)×高", "棱长×4"], 1,
        "长方体体积=长×宽×高。",
        "常见误区是漏乘高，或长度单位不统一就相乘，以及体积单位写成面积单位。应三边乘完并用立方单位。",
        "solid", "长方体体积", "立体轮廓示意长、宽、高三个方向，体积是三者之积。"),
    "math-elem-volume-units": C(
        "体积单位与容积", "体积单位常用立方厘米（cm³）、立方分米（dm³）、立方米（m³）。进率：1立方分米=1000立方厘米，1立方米=1000立方分米。容积是容器所能容纳物体的体积，单位常用升（L）、毫升（mL）：1升=1立方分米，1毫升=1立方厘米，1升=1000毫升。",
        "方法：分清体积与容积并换算", "固体所占空间用体积单位；容器能装多少用容积（升、毫升）。换算按千进：相邻体积单位多为1000倍。选单位要合适：橡皮用立方厘米，游泳池用立方米，饮料用升或毫升。",
        "2升=2000毫升=2000立方厘米；边长1分米的正方体容积是1升。500毫升矿泉水=0.5升。",
        "1升等于多少毫升？", ["10", "100", "1000", "10000"], 2,
        "1升=1000毫升=1立方分米。",
        "常见误区是体积单位按100倍换算（与面积混淆），或升和毫升关系记错。应记住体积相邻单位千进，1升=1000毫升。",
        "solid", "体积与容积", "容器轮廓帮助区分物体体积和容器容积。"),
    "math-elem-word-problems-basic": C(
        "简单应用题：加与减", "简单加减应用题描述生活中的合并、增加、去掉、比较等情境。合并、增加常用加法；去掉、求出还剩多少常用减法；比较多多少、少多少用减法。解题关键是读懂谁和谁、发生了什么变化。",
        "方法：抓关键词、列式检验", "圈出数量和关键词（一共、还剩、多、少等），判断用加还是减；列式计算后把结果放回题中看是否合理，也可用加减互逆验算。画简单线段图能帮助理解。",
        "小明有18支铅笔，又买了7支，一共18+7=25支；用去9支，还剩25-9=16支。学校有30人，男生比女生多6人，可结合线段图分析。",
        "“还剩多少”一般用什么运算？", ["加法", "减法", "乘法", "随便"], 1,
        "从原有数量中去掉一部分求剩余，用减法。",
        "常见误区是看见大数字就用减法、看见“一共”就加却不加分析比较类题目。应紧扣题意判断数量关系，不能只靠个别词。",
        "numberline", "加减线段图", "在数轴上向右表示增加、向左表示减少，理解简单加减应用题。"),
    "math-elem-word-problems-multiply": C(
        "乘法应用题", "乘法应用题常见类型：求几个相同加数的和（每份数×份数=总数）、已知单价和数量求总价、已知速度和时间求路程等。题目中常出现“每、各、倍”等词。能用乘法的也可以写成连加，但乘法更简便。",
        "方法：找“每份”与“份数”", "先找出每份是多少、有这样的几份，再列式：每份数×份数=总数。单价×数量=总价，速度×时间=路程，本质相同。可用除法验算：总数÷每份数=份数。注意单位：总价带“元”，路程带长度单位。",
        "每盒6支铅笔，5盒一共6×5=30支；一本书12元，买4本共12×4=48元；每小时走4千米，3小时走12千米。",
        "求几个相同加数的和，用？", ["只有加法", "乘法（也可连加）", "只有减法", "除法"], 1,
        "几个相同加数相加可用乘法计算，更简便。",
        "常见误区是把“倍”理解错（如5的3倍写成5+3），或份数与每份数乘反但得数碰巧对却说不清意义。应明确谁是每份数、谁是份数。",
        "grid", "每份与份数", "阵列中每行个数×行数=总数，对应乘法应用题模型。"),
}

KIND = {c: cfg["kind"] for c, cfg in COURSES.items()}


STYLE = """
<style id="mathelem-depth-css">
.mathelem-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.mathelem-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(45,212,191,.08);border:1px solid rgba(45,212,191,.24)}
.mathelem-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.mathelem-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.mathelem-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.mathelem-depth .mathelem-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.mathelem-depth .mathelem-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
.mathelem-depth .me-visual-canvas{width:100%;max-width:560px;height:auto;background:#0b1628;border:1px solid rgba(148,163,184,.28);border-radius:12px;display:block;margin:8px auto 0}
</style>
"""

CHECK_SCRIPT = """
<script id="mathelem-depth-js">
function mathelemDepthCheck(button, isCorrect, feedbackId, explanation) {
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
(function () {
  function draw(cv) {
    var kind = cv.getAttribute('data-kind');
    var ctx = cv.getContext('2d');
    var W = cv.width, H = cv.height;
    ctx.clearRect(0, 0, W, H);
    ctx.strokeStyle = '#94a3b8'; ctx.fillStyle = '#e5e7eb';
    ctx.lineWidth = 2; ctx.font = '13px sans-serif'; ctx.textAlign = 'center';
    if (kind === 'numberline') {
      var y = H / 2, x0 = 40, x1 = W - 40, n = 10;
      ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x1, y); ctx.stroke();
      for (var i = 0; i <= n; i++) {
        var x = x0 + (x1 - x0) * i / n;
        ctx.beginPath(); ctx.moveTo(x, y - 8); ctx.lineTo(x, y + 8); ctx.stroke();
        ctx.fillText(String(i), x, y + 26);
      }
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath(); ctx.arc(x0 + (x1 - x0) * 0.7, y, 6, 0, Math.PI * 2); ctx.fill();
    } else if (kind === 'protractor') {
      var cx = W / 2, cy = H - 30, r = Math.min(W, H) - 60;
      ctx.beginPath(); ctx.arc(cx, cy, r, Math.PI, 2 * Math.PI); ctx.stroke();
      for (var a = 0; a <= 180; a += 30) {
        var rad = Math.PI + a * Math.PI / 180;
        ctx.beginPath();
        ctx.moveTo(cx + r * Math.cos(rad), cy + r * Math.sin(rad));
        ctx.lineTo(cx + (r - 12) * Math.cos(rad), cy + (r - 12) * Math.sin(rad));
        ctx.stroke();
        ctx.fillText(String(a), cx + (r + 14) * Math.cos(rad), cy + (r + 14) * Math.sin(rad) + 4);
      }
      ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + r, cy); ctx.stroke();
      var ar = Math.PI + 60 * Math.PI / 180;
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + r * Math.cos(ar), cy + r * Math.sin(ar)); ctx.stroke();
    } else if (kind === 'grid') {
      var g = 28, cols = Math.floor((W - 40) / g), rows = Math.floor((H - 40) / g);
      ctx.strokeStyle = 'rgba(148,163,184,.4)';
      for (var c = 0; c <= cols; c++) { ctx.beginPath(); ctx.moveTo(20 + c * g, 20); ctx.lineTo(20 + c * g, 20 + rows * g); ctx.stroke(); }
      for (var rr = 0; rr <= rows; rr++) { ctx.beginPath(); ctx.moveTo(20, 20 + rr * g); ctx.lineTo(20 + cols * g, 20 + rr * g); ctx.stroke(); }
      ctx.fillStyle = 'rgba(56,189,248,.25)'; ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2;
      ctx.fillRect(20, 20, 5 * g, 3 * g); ctx.strokeRect(20, 20, 5 * g, 3 * g);
      ctx.fillStyle = '#e5e7eb'; ctx.fillText('长5 × 宽3 = 15 个方格', 20 + 2.5 * g, 20 + 3 * g + 20);
    } else if (kind === 'solid') {
      // 圆柱
      var lx = W * 0.28, ry = 18, rx = 44, top = 40, bot = H - 50;
      ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.ellipse(lx, top, rx, ry, 0, 0, Math.PI * 2); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(lx - rx, top); ctx.lineTo(lx - rx, bot); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(lx + rx, top); ctx.lineTo(lx + rx, bot); ctx.stroke();
      ctx.beginPath(); ctx.ellipse(lx, bot, rx, ry, 0, 0, Math.PI); ctx.stroke();
      ctx.fillStyle = '#e5e7eb'; ctx.fillText('圆柱', lx, bot + 26);
      // 圆锥
      var cx2 = W * 0.72;
      ctx.strokeStyle = '#f472b6';
      ctx.beginPath(); ctx.ellipse(cx2, bot, rx, ry, 0, 0, Math.PI * 2); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(cx2 - rx, bot); ctx.lineTo(cx2, top); ctx.lineTo(cx2 + rx, bot); ctx.stroke();
      ctx.fillText('圆锥', cx2, bot + 26);
    } else if (kind === 'linechart') {
      var ox = 40, oy = H - 36, ax = W - 24, ay = 24;
      ctx.beginPath(); ctx.moveTo(ox, ay); ctx.lineTo(ox, oy); ctx.lineTo(ax, oy); ctx.stroke();
      var data = [3, 5, 4, 7, 9, 8, 11], m = data.length;
      ctx.strokeStyle = '#38bdf8'; ctx.fillStyle = '#38bdf8'; ctx.lineWidth = 3;
      ctx.beginPath();
      for (var k = 0; k < m; k++) {
        var px = ox + (ax - ox) * k / (m - 1);
        var py = oy - (oy - ay) * data[k] / 12;
        if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();
      for (var k2 = 0; k2 < m; k2++) {
        var px2 = ox + (ax - ox) * k2 / (m - 1);
        var py2 = oy - (oy - ay) * data[k2] / 12;
        ctx.beginPath(); ctx.arc(px2, py2, 4, 0, Math.PI * 2); ctx.fill();
      }
    } else if (kind === 'pie') {
      var pcx = W / 2, pcy = H / 2, pr = Math.min(W, H) / 2 - 28;
      var slices = [0.35, 0.25, 0.20, 0.20], colors = ['#38bdf8', '#f472b6', '#fbbf24', '#34d399'];
      var start = -Math.PI / 2;
      for (var si = 0; si < slices.length; si++) {
        var ang = slices[si] * Math.PI * 2;
        ctx.beginPath(); ctx.moveTo(pcx, pcy);
        ctx.arc(pcx, pcy, pr, start, start + ang); ctx.closePath();
        ctx.fillStyle = colors[si]; ctx.fill();
        ctx.strokeStyle = '#0b1628'; ctx.lineWidth = 2; ctx.stroke();
        start += ang;
      }
      ctx.fillStyle = '#e5e7eb'; ctx.fillText('部分占总体', pcx, H - 12);
    } else if (kind === 'bars') {
      var bdata = [5, 3, 7, 4], labels = ['甲', '乙', '丙', '丁'];
      var box = 40, boy = H - 36, bax = W - 24, bay = 28, bw = 48, gap = 36;
      ctx.strokeStyle = '#94a3b8';
      ctx.beginPath(); ctx.moveTo(box, bay); ctx.lineTo(box, boy); ctx.lineTo(bax, boy); ctx.stroke();
      for (var bi = 0; bi < bdata.length; bi++) {
        var bx = box + 30 + bi * (bw + gap);
        var bh = (boy - bay) * bdata[bi] / 8;
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(bx, boy - bh, bw, bh);
        ctx.fillStyle = '#e5e7eb';
        ctx.fillText(labels[bi], bx + bw / 2, boy + 18);
        ctx.fillText(String(bdata[bi]), bx + bw / 2, boy - bh - 8);
      }
    } else if (kind === 'circle') {
      var ccx = W / 2, ccy = H / 2, cr = Math.min(W, H) / 2 - 36;
      ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(ccx, ccy, cr, 0, Math.PI * 2); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(ccx, ccy); ctx.lineTo(ccx + cr, ccy); ctx.stroke();
      ctx.fillStyle = '#e5e7eb';
      ctx.fillText('r', ccx + cr / 2, ccy - 8);
      ctx.fillText('S = πr²', ccx, ccy + cr + 22);
      ctx.beginPath(); ctx.arc(ccx, ccy, 3, 0, Math.PI * 2); ctx.fill();
    } else if (kind === 'shapes') {
      ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2;
      ctx.strokeRect(30, 50, 100, 70);
      ctx.fillStyle = '#e5e7eb'; ctx.fillText('长方形', 80, 140);
      ctx.strokeRect(160, 50, 70, 70);
      ctx.fillText('正方形', 195, 140);
      ctx.beginPath(); ctx.moveTo(280, 120); ctx.lineTo(320, 50); ctx.lineTo(360, 120); ctx.closePath(); ctx.stroke();
      ctx.fillText('三角形', 320, 140);
      ctx.beginPath(); ctx.arc(450, 85, 40, 0, Math.PI * 2); ctx.stroke();
      ctx.fillText('圆', 450, 140);
    }
  }
  function init() {
    document.querySelectorAll('canvas.me-visual-canvas').forEach(draw);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>
"""


def build_block(cfg: dict, course_id: str) -> str:
    feedback_id = "mathelem-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "mathelemDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false", f=feedback_id,
            e=json.dumps(cfg["feedback"], ensure_ascii=False))
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0", h=html.escape(handler, quote=True),
                letter=chr(65 + idx), opt=html.escape(opt)))
    canvas_id = "me-canvas-" + course_id
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section mathelem-depth core-knowledge-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section mathelem-depth core-knowledge-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="mathelem-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="mathelem-feedback" id="{feedback_id}" role="status"></div>
      </div>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="可视化">
  <section class="section mathelem-depth" id="lesson-visual" data-tts="lesson-visual">
    <div class="card">
      <span class="phase-tag" data-variant="success">互动可视</span>
      <h2>{html.escape(cfg['viz_title'])}</h2>
      <p>{html.escape(cfg['viz_desc'])}</p>
      <canvas class="me-visual-canvas" id="{canvas_id}" width="560" height="240"
        data-kind="{cfg['kind']}" role="img" aria-label="{html.escape(cfg['viz_title'])}"></canvas>
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
    block = build_block(cfg, course_id)
    source = source[:insert_at] + block + "\n" + source[insert_at:]
    if 'id="mathelem-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="mathelem-depth-js"' not in source:
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
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True, "2 modules + canvas + metadata"


def main() -> int:
    changed = failed = 0
    for course_id, cfg in COURSES.items():
        ok, msg = upgrade(course_id, cfg)
        if ok:
            changed += 1
        elif msg == "already upgraded":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
