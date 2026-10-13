#!/usr/bin/env python3
"""Add depth modules + a canvas visualization to failing math-elem courses.

These elementary-math courses fail with: substantial sections < 5, text < 1800,
and (5 of 8) B-3a visualization units < 3. Each course gets a concept module, a
method module (worked example + diagnostic + 常见误区) and one interactive
<canvas> visualization module (number line / protractor / area grid / solids /
line chart). The canvas raises visualization units by 1. No mp4.
Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-09"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit, kind, viz_title, viz_desc):
    return dict(concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
                example=ex, question=q, options=opts, correct=correct, feedback=fb,
                pitfall=pit, kind=kind, viz_title=viz_title, viz_desc=viz_desc)


COURSES = {
    "math-elem-add-sub-within-20": C(
        "20以内加减法：凑十与破十", "20以内的加减法是计算的基础。进位加法常用“凑十法”：把一个加数凑成10，再加剩下的数，如 9+5，把9凑成10需要1，5拆成1和4，得10+4=14。退位减法常用“破十法”：不够减时从十位借10来减，如 13-8，用10-8=2，再加个位3得5。",
        "方法：先凑十、后计算", "做进位加法先看哪个数更接近10，把它凑成10，另一个数拆成“补数+剩余”；做退位减法先用10减去减数，再加上被减数的个位。多用小棒、计数器摆一摆，理解“满十进一、退一当十”的道理，算得又对又快。",
        "计算 8+7：把8凑成10需要2，7拆成2和5，得 10+5=15；计算 15-9：10-9=1，1+5=6。",
        "用凑十法算 9+6，应把 6 拆成？", ["1和5", "2和4", "3和3", "4和2"], 0,
        "9凑成10需要1，所以把6拆成1和5，得10+5=15。",
        "常见误区是进位时忘记“满十进一”、退位时忘记“退一当十”，导致个位十位算错。应借助凑十、破十的过程理解进退位的道理，动手摆一摆，把方法用熟。",
        "numberline", "数轴上的20以内数", "数轴帮助我们看清数的顺序，加法就是向右移、减法就是向左移。"),
    "math-elem-add-sub-within-100": C(
        "100以内加减法：竖式与进退位", "100以内加减法要理解数位对齐和进位退位。列竖式时相同数位对齐，从个位算起。加法个位满十向十位进一；减法个位不够减时从十位退一当十再减。理解算理比死记步骤更重要。",
        "方法：数位对齐、逐位计算", "计算时先把两数按数位对齐写成竖式，从个位开始：加法逐位相加，满十进一；减法逐位相减，不够减就向前一位借一当十。算完再估算检验结果是否合理，养成验算的好习惯。",
        "计算 47+38：个位7+8=15，写5进1；十位4+3+1=8，得85。计算 62-25：个位2不够减25的5，退一当十，12-5=7；十位5-2=3，得37。",
        "计算 53-27 时，个位应怎样处理？", ["直接3-7", "从十位退一，13-7", "十位减个位", "结果为0"], 1,
        "个位3不够减7，从十位退一当十，用13-7=6。",
        "常见误区是竖式数位没对齐，或进位、退位时漏加漏减。应牢记相同数位对齐、从个位算起、满十进一/退一当十，算完用估算或逆运算验算。",
        "numberline", "数轴与100以内的数", "借助数轴看清数位与加减的移动，理解进位退位的过程。"),
    "math-elem-angles": C(
        "角的认识与度量", "角是由一个顶点和两条边组成的图形。角的大小与两边张开的程度有关，与边画得长短无关。度量角的单位是度（°），量角器上有0到180度的刻度。按大小可把角分为锐角（小于90°）、直角（等于90°）、钝角（大于90°小于180°）等。",
        "方法：用量角器正确量角", "量角要做到“两重合、看刻度”：量角器中心点与角的顶点重合，0刻度线与角的一条边重合，再看另一条边所对的刻度。读数时注意分辨内圈还是外圈刻度，从与边重合的0刻度开始数。",
        "量一个角时，中心对准顶点、0°线压住一条边，另一条边指向60°，这个角就是60°，是锐角。",
        "角的大小取决于？", ["边画得长短", "两边张开的程度", "顶点位置", "纸的大小"], 1,
        "角的大小只与两边张开的程度有关，与边长无关。",
        "常见误区是认为边画得越长角越大，或量角时中心、0刻度线没对齐、内外圈刻度看错。应记住角的大小与边长无关，量角要“中心对顶点、0线压一边、看另一边刻度”。",
        "protractor", "量角器与角", "量角器上的角：中心对准顶点、0刻度线压住一条边，再看另一条边所对的刻度。"),
    "math-elem-area-calculation": C(
        "面积计算：长方形与正方形", "面积是物体表面或封闭图形的大小，常用单位有平方厘米、平方分米、平方米。长方形的面积=长×宽，正方形的面积=边长×边长。求面积前要统一长度单位，结果的单位是面积单位。",
        "方法：先量再套公式", "计算面积先确认图形形状，量出所需的边长并统一单位，再套用公式计算。遇到组合图形，可把它分割成几个长方形或正方形分别计算再相加，或用大图形减去空缺部分。",
        "一个长方形长5厘米、宽3厘米，面积=5×3=15平方厘米；边长4厘米的正方形面积=4×4=16平方厘米。",
        "长方形面积的计算公式是？", ["长+宽", "长×宽", "(长+宽)×2", "长×长"], 1,
        "长方形面积=长×宽，(长+宽)×2是周长。",
        "常见误区是把面积和周长公式混淆，或计算时长度单位不统一。应分清面积=长×宽、周长=(长+宽)×2，先统一单位，面积结果用面积单位。",
        "grid", "面积网格", "在方格纸上数格子：长5、宽3的长方形正好铺满15个方格，即面积=长×宽。"),
    "math-elem-cylinder-cone": C(
        "圆柱与圆锥：表面积与体积", "圆柱有两个相同的圆面（底面）和一个曲面（侧面），侧面展开是长方形。圆柱体积=底面积×高。圆锥有一个圆底面和一个曲面，体积=底面积×高×1/3。等底等高的圆锥体积是圆柱体积的三分之一。",
        "方法：抓底面积和高", "求圆柱圆锥的体积，先算底面积（πr²），再乘高；圆锥别忘了乘1/3。求圆柱表面积=侧面积(底面周长×高)+两个底面积。计算前统一单位，注意区分半径和直径。",
        "底面半径2厘米、高5厘米的圆柱，体积=π×2²×5≈62.8立方厘米；等底等高的圆锥体积≈20.9立方厘米。",
        "等底等高时，圆锥的体积是圆柱的？", ["相等", "三分之一", "两倍", "三倍"], 1,
        "等底等高时圆锥体积是圆柱的三分之一。",
        "常见误区是求圆锥体积忘乘1/3，或把半径与直径混用。应牢记圆锥体积=底面积×高×1/3，先看清给的是半径还是直径，并统一单位。",
        "solid", "圆柱与圆锥", "对比圆柱与圆锥的形状：等底等高时，圆锥的体积只有圆柱的三分之一。"),
    "math-elem-decimals-intro": C(
        "小数的初步认识", "小数是表示比1小或带有零头的数，由整数部分、小数点和小数部分组成，如3.5读作“三点五”。一位小数表示十分之几，如0.1就是1/10。生活中的价格、身高常用小数表示，元角分与小数关系密切：1角=0.1元，1分=0.01元。",
        "方法：联系分数与元角分理解", "认识小数可借助元角分和米尺：几角就是零点几元，如7角=0.7元；把1米平均分成10份，每份1分米=0.1米。读小数时整数部分照读，小数点读“点”，小数部分按数字依次读。",
        "5角3分写成小数是0.53元；1.2米表示1米又2分米，其中0.2米就是2分米。",
        "0.1表示的是？", ["十分之一", "百分之一", "十", "一百"], 0,
        "一位小数0.1表示十分之一（1/10）。",
        "常见误区是把小数点后的数字当成整数来读，如把0.53读成“零点五十三”。应按数字依次读作“零点五三”，并借助元角分、米尺理解小数的实际含义。",
        "numberline", "0到1的小数", "把0到1平均分成10份，每一份就是0.1，数轴上的点帮助我们认识一位小数。"),
    "math-elem-decimals-meaning": C(
        "小数的意义和性质", "小数的计数单位是十分之一、百分之一、千分之一……分别写作0.1、0.01、0.001。小数点后第一位是十分位、第二位是百分位。小数的性质是：小数末尾添上或去掉0，小数的大小不变，如0.30=0.3。利用这一性质可以化简和改写小数。",
        "方法：用数位和性质比较化简", "比较小数大小先比整数部分，整数部分相同再依次比较十分位、百分位……。化简小数就是去掉末尾的0，如1.500化简为1.5；把小数改写成指定位数时，可在末尾添0而不改变大小。",
        "比较0.6和0.58：整数部分都是0，十分位6>5，所以0.6>0.58；化简2.40得2.4。",
        "根据小数的性质，下列相等的是？", ["0.5和0.05", "0.30和0.3", "1.2和12", "0.1和1"], 1,
        "小数末尾去掉0大小不变，故0.30=0.3。",
        "常见误区是认为小数末尾添0会变大、比较小数时按位数多少判断大小。应记住小数末尾添去0大小不变，比较时从高位（整数、十分位）依次比，而非看小数位数多少。",
        "numberline", "小数的数位", "用数轴理解十分位、百分位：位置越靠右的数位越小，比较大小要从高位依次比。"),
    "math-elem-line-graph": C(
        "折线统计图", "折线统计图用点表示数量、用线段把点连起来，不仅能表示数量的多少，还能清楚地反映数量的增减变化趋势。它适合表示一段时间内同一事物数量的变化，如气温、身高的变化。",
        "方法：读图看点与趋势", "看折线图先看标题和横纵轴表示什么，再看各点对应的数值，最后看线的走势：上升表示增加、下降表示减少、平直表示不变，坡度越陡变化越大。据此可以分析变化并进行简单预测。",
        "某地一周气温折线图中，线从周一到周三持续上升，说明这三天气温逐渐升高，周三坡度最陡说明升幅最大。",
        "折线统计图最突出的优点是？", ["只能看总数", "能反映数量的增减变化趋势", "不能比较大小", "只适合分类数据"], 1,
        "折线统计图能清楚反映数量的增减变化趋势。",
        "常见误区是只读折线图上的单个数值，忽视线的走势所反映的变化趋势。应结合横纵轴和线的升降、陡缓，分析数量的增减变化，这正是折线图的长处。",
        "linechart", "折线统计图示例", "点表示各时刻的数量，线段的升降和陡缓反映数量增减的快慢趋势。"),
}

# 每门可视化画布类型
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
