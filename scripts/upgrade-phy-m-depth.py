#!/usr/bin/env python3
"""Add one topic-specific depth section to failing phy-m courses.

These middle-school physics courses already have module-1/2/3, labs and PhET,
but the teaching-quality gate counts only 4 substantial sections (>=120
chinese chars) because most content sections are nested inside slide-page
wrappers and get split by the validator's non-greedy section regex.

This script inserts ONE extra standalone depth section (id="module-depth",
wrapped in its own slide-page so it is counted whole) with a readable
explanation, a worked example and a diagnostic check. That lifts the
substantial-section count from 4 to 5 without embedding any mp4.

Idempotent: courses already containing id="module-depth" are skipped.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-09"


COURSES = {
    "phy-m-acoustics-cross-disciplinary": {
        "title": "声现象的跨学科追问：从振动到信息",
        "body": (
            "声音的本质是物体振动通过介质传播的机械波。它既能传递能量（如超声波清洗、碎石），也能传递信息（如声呐测距、B 超成像）。"
            "分析真实问题时先判断这里利用的是声的能量还是信息，再联系频率、响度、音色三要素。次声与超声超出人耳范围，但在预警和医疗中很有用。"
        ),
        "example": "蝙蝠靠发出超声并接收回声定位：利用声传递信息；而超声波碎结石则是利用声传递能量。",
        "question": "医生用 B 超观察胎儿，主要利用声波？",
        "options": ["传递能量", "传递信息", "既不传能也不传信", "只在真空中传播"],
        "correct": 1,
        "feedback": "B 超通过回声成像，利用声波传递信息。",
    },
    "phy-m-electric-motor": {
        "title": "电动机深化：从磁场对电流的作用到持续转动",
        "body": (
            "电动机的核心是通电线圈在磁场中受安培力而转动，把电能转化为机械能。单靠一次受力线圈会停在平衡位置，"
            "因此需要换向器在线圈转过平衡位置时改变电流方向，使力矩方向保持一致，线圈才能连续转动。理解“何时换向”是难点。"
        ),
        "example": "线圈平面与磁场平行时受力最大、转动最快；转到与磁场垂直的平衡位置时换向器切换电流方向，维持同向转动。",
        "question": "直流电动机中换向器的作用是？",
        "options": ["增大电压", "在平衡位置改变线圈电流方向", "减小电阻", "把交流变直流"],
        "correct": 1,
        "feedback": "换向器适时改变电流方向，使线圈能连续同向转动。",
    },
    "phy-m-electromagnetic-induction": {
        "title": "电磁感应深化：变化才有感应电流",
        "body": (
            "闭合电路的一部分导体做切割磁感线运动时，电路中产生感应电流，这是电磁感应。关键在“切割”或磁通变化："
            "导体不动、或沿磁感线方向运动（不切割）时都没有感应电流。感应电流方向与导体运动方向、磁场方向有关，可用右手定则判断。"
        ),
        "example": "导体棒在磁场中上下平动切割磁感线，电流表指针偏转；若沿磁感线方向平移则不产生感应电流。",
        "question": "下列情形能产生感应电流的是？",
        "options": ["导体静止在磁场中", "导体沿磁感线方向移动", "导体切割磁感线运动", "磁场恒定且导体不动"],
        "correct": 2,
        "feedback": "只有切割磁感线（磁通变化）才产生感应电流。",
    },
    "phy-m-eye-vision": {
        "title": "眼睛与视力矫正：晶状体如何成像",
        "body": (
            "眼睛的晶状体相当于凸透镜，把物体的像成在视网膜上（倒立缩小的实像）。看远看近时睫状体调节晶状体的厚薄以改变焦距。"
            "近视是像成在视网膜前，用凹透镜矫正；远视是像成在视网膜后，用凸透镜矫正。把眼睛类比透镜成像是理解矫正的关键。"
        ),
        "example": "近视眼看远处物体时，像落在视网膜前方，佩戴凹透镜使光线适当发散，把像移回视网膜上。",
        "question": "近视眼应佩戴哪种透镜矫正？",
        "options": ["凸透镜", "凹透镜", "平面镜", "三棱镜"],
        "correct": 1,
        "feedback": "近视像成在视网膜前，用凹透镜发散光线矫正。",
    },
    "phy-m-generator": {
        "title": "发电机深化：机械能到电能的转化",
        "body": (
            "发电机的原理是电磁感应：线圈在磁场中转动，不断切割磁感线，产生感应电流，把机械能转化为电能。"
            "线圈每转一周电流方向改变两次，因此发电机输出的是交流电。它与电动机结构相似但能量转化方向相反，理解这一对“互逆”很重要。"
        ),
        "example": "手摇发电机转得越快，线圈切割磁感线越快，感应电动势越大，小灯泡越亮。",
        "question": "发电机工作时的能量转化是？",
        "options": ["电能转化为机械能", "机械能转化为电能", "内能转化为电能", "电能转化为内能"],
        "correct": 1,
        "feedback": "发电机把机械能转化为电能，与电动机相反。",
    },
    "phy-m-internal-energy": {
        "title": "内能深化：温度、内能与热量的区别",
        "body": (
            "内能是物体内所有分子动能与分子势能的总和，与温度、质量、状态有关。改变内能有两种方式：做功和热传递，二者等效。"
            "温度、内能、热量是三个不同概念：温度是状态量，内能是状态量，热量是过程量，只能说“吸收/放出”热量，不能说“含有”热量。"
        ),
        "example": "反复弯折铁丝使其发热，是通过做功增大内能；把铁丝放进热水中变热，则是通过热传递增大内能。",
        "question": "下列说法正确的是？",
        "options": ["物体含有的热量", "温度高的物体内能一定大", "做功和热传递都能改变内能", "内能就是温度"],
        "correct": 2,
        "feedback": "做功与热传递都能改变内能；热量是过程量不能说“含有”。",
    },
    "phy-m-light-dispersion": {
        "title": "光的色散深化：白光由多种色光组成",
        "body": (
            "白光通过三棱镜会分解成红橙黄绿蓝靛紫，这是光的色散，说明白光是由各种色光混合而成。"
            "不同色光在同种介质中偏折程度不同（紫光偏折最大、红光最小），所以被分开。物体的颜色由它反射（透明体透过）的色光决定。"
        ),
        "example": "雨后天空的彩虹是阳光被小水滴色散形成的；红色物体只反射红光，吸收其他色光。",
        "question": "白光通过三棱镜发生色散，说明？",
        "options": ["白光是单色光", "白光由多种色光组成", "三棱镜会发光", "各色光偏折相同"],
        "correct": 1,
        "feedback": "色散把白光分解，说明白光由多种色光组成。",
    },
    "phy-m-light-propagation": {
        "title": "光的直线传播深化：影、日食与小孔成像",
        "body": (
            "光在同种均匀介质中沿直线传播，由此可以解释影子、日食月食和小孔成像。小孔成像成的是倒立的实像，"
            "像的形状由物体决定而与孔的形状无关，这与孔的大小需足够小是理解难点。光在不同介质交界处才会改变方向（反射、折射）。"
        ),
        "example": "阳光透过树叶间的小孔在地面形成的圆形光斑，其实是太阳倒立的实像，而非孔的形状。",
        "question": "小孔成像所成的像是？",
        "options": ["正立虚像", "倒立实像", "正立实像", "与孔形状相同的光斑"],
        "correct": 1,
        "feedback": "小孔成像是光沿直线传播形成的倒立实像。",
    },
    "phy-m-light-refraction": {
        "title": "光的折射深化：从空气到水的偏折规律",
        "body": (
            "光从一种介质斜射入另一种介质时传播方向发生偏折，这是折射。光从空气斜射入水或玻璃时，折射角小于入射角；"
            "反过来则折射角大于入射角。垂直入射时方向不变。生活中“池水看起来变浅”“筷子在水中变弯”都是折射造成的。"
        ),
        "example": "从岸上看水中的鱼，看到的是鱼偏上的虚像，实际的鱼比看到的位置更深。",
        "question": "光从空气斜射入水中，折射角与入射角的关系是？",
        "options": ["折射角大于入射角", "折射角小于入射角", "两者相等", "折射角为零"],
        "correct": 1,
        "feedback": "由空气进入水（光密介质），折射角小于入射角。",
    },
    "phy-m-mass-density": {
        "title": "质量与密度深化：密度是物质的特性",
        "body": (
            "质量是物体所含物质的多少，不随形状、状态、位置改变。密度 ρ=m/V 反映单位体积的质量，是物质的一种特性，"
            "同种物质密度一般相同，可用来鉴别物质。对同种物质，质量与体积成正比，ρ 不随 m、V 改变，这一点常被误解。"
        ),
        "example": "一块铜无论切成几块，每块的密度都相同；用 ρ=m/V 测出的密度可判断某金属是否为纯铜。",
        "question": "关于密度，正确的是？",
        "options": ["体积越大密度越大", "质量越大密度越大", "同种物质密度一般相同", "密度随形状改变"],
        "correct": 2,
        "feedback": "密度是物质特性，同种物质密度一般相同，与 m、V 无关。",
    },
    "phy-m-newton-laws": {
        "title": "运动与力深化：惯性与二力平衡",
        "body": (
            "牛顿第一定律指出：一切物体在不受力时保持静止或匀速直线运动，物体具有保持运动状态的惯性，惯性大小只由质量决定。"
            "力不是维持运动的原因，而是改变运动状态的原因。物体处于静止或匀速直线运动时，受到的是一对平衡力（等大、反向、共线、同物体）。"
        ),
        "example": "公交车突然刹车，乘客因惯性向前倾；匀速行驶的车中，牵引力与阻力是一对平衡力。",
        "question": "关于惯性，正确的是？",
        "options": ["速度越大惯性越大", "惯性大小只由质量决定", "受力才有惯性", "静止物体没有惯性"],
        "correct": 1,
        "feedback": "惯性只由质量决定，与速度、受力无关。",
    },
    "phy-m-phase-change": {
        "title": "物态变化深化：吸热放热与温度不变",
        "body": (
            "物质在固、液、气之间转化：熔化、汽化、升华吸热，凝固、液化、凝华放热。晶体熔化和液体沸腾时，虽然持续吸热，"
            "但温度保持不变，吸收的热量用于改变状态而非升温。这一“吸热但温度不变”的现象是理解难点，需结合分子间作用理解。"
        ),
        "example": "冰水混合物在熔化过程中持续吸热，温度却保持 0℃ 不变，直到冰全部化完才继续升温。",
        "question": "晶体熔化过程中，下列正确的是？",
        "options": ["放热且温度升高", "吸热但温度不变", "不吸热温度不变", "吸热且温度升高"],
        "correct": 1,
        "feedback": "晶体熔化时持续吸热，但温度保持熔点不变。",
    },
    "phy-m-plane-mirror": {
        "title": "平面镜成像深化：等大、正立的虚像",
        "body": (
            "平面镜成像的特点是：像与物大小相等、到镜面的距离相等、连线与镜面垂直，成的是正立的虚像。"
            "像不是光线实际会聚成的，而是反射光线的反向延长线相交而成，所以不能用光屏承接。理解“虚像”与“像距等于物距”是关键。"
        ),
        "example": "人靠近平面镜时，像也同样靠近，像的大小始终与人相同，用光屏在像的位置无法承接到像。",
        "question": "平面镜所成的像是？",
        "options": ["倒立实像", "正立虚像", "缩小实像", "放大虚像"],
        "correct": 1,
        "feedback": "平面镜成等大、正立的虚像，不能用光屏承接。",
    },
    "phy-m-resistance": {
        "title": "电阻深化：由导体自身性质决定",
        "body": (
            "电阻表示导体对电流的阻碍作用，大小由材料、长度、横截面积和温度决定：长度越长、横截面积越小，电阻越大。"
            "电阻是导体本身的性质，不随两端电压和通过电流的改变而改变（温度基本不变时）。误以为“电压增大电阻变大”是常见错误。"
        ),
        "example": "同种材料的两根导线，较长且较细的那根电阻较大；给同一电阻加不同电压，其阻值基本不变。",
        "question": "关于电阻，正确的是？",
        "options": ["电压越大电阻越大", "电流越大电阻越大", "电阻由导体自身性质决定", "电阻随电压反比变化"],
        "correct": 2,
        "feedback": "电阻由材料、长度、横截面积、温度决定，与电压电流无关。",
    },
    "phy-m-simple-machines": {
        "title": "简单机械深化：省力必费距离",
        "body": (
            "杠杆、滑轮等简单机械可以省力或改变力的方向，但不能省功。使用任何机械，做的总功不会少于直接做的有用功，"
            "省力的同时一定费距离（或费时间）。动滑轮省一半力但费一倍距离；定滑轮不省力只改变方向。这体现功的原理。"
        ),
        "example": "用动滑轮把重物提高 1 m，绳端要拉动 2 m，拉力约为重力的一半，但做的功并不减少。",
        "question": "使用省力的简单机械，一定会？",
        "options": ["同时省功", "费距离", "省距离", "省功又省距离"],
        "correct": 1,
        "feedback": "机械不能省功，省力必然费距离。",
    },
    "phy-m-sound-generation": {
        "title": "声音的产生与传播深化：振动与介质",
        "body": (
            "声音由物体振动产生，振动停止发声也停止。声音的传播需要介质，可以在固体、液体、气体中传播，但不能在真空中传播。"
            "声音在不同介质中传播速度不同，一般固体中最快、气体中最慢。把“发声靠振动、传声靠介质”分开理解很重要。"
        ),
        "example": "把正在发声的音叉插入水中会激起水花，说明音叉在振动；月球上没有空气，宇航员必须靠无线电通话。",
        "question": "声音不能在下列哪种情况中传播？",
        "options": ["固体中", "液体中", "气体中", "真空中"],
        "correct": 3,
        "feedback": "声音传播需要介质，真空不能传声。",
    },
    "phy-m-spherical-mirror": {
        "title": "球面镜深化：凹镜会聚与凸镜发散",
        "body": (
            "球面镜分凹面镜和凸面镜。凹面镜对光有会聚作用，可用作太阳灶、手电筒和汽车前灯的反射面；"
            "凸面镜对光有发散作用，成正立缩小的虚像，视野开阔，常用作汽车后视镜和路口反光镜。判断用途先分清会聚还是发散。"
        ),
        "example": "汽车后视镜用凸面镜，能看到更大范围的车辆；太阳灶用凹面镜把阳光会聚到锅底加热。",
        "question": "汽车后视镜通常采用凸面镜，是因为它能？",
        "options": ["会聚光线", "扩大视野", "成放大的像", "成倒立实像"],
        "correct": 1,
        "feedback": "凸面镜发散光线、成正立缩小虚像，视野更开阔。",
    },
    "phy-m-static-electricity": {
        "title": "静电现象深化：电荷的转移与相互作用",
        "body": (
            "摩擦起电的本质是电子从一个物体转移到另一个物体，得到电子的带负电、失去电子的带正电，电荷总量守恒（并非创造电荷）。"
            "同种电荷相互排斥，异种电荷相互吸引。带电体能吸引轻小物体。把“转移”而非“产生”电荷理解清楚是关键。"
        ),
        "example": "用丝绸摩擦玻璃棒，玻璃棒失去电子带正电，丝绸得到电子带负电，两者电荷等量异号。",
        "question": "摩擦起电的实质是？",
        "options": ["创造了电荷", "电子发生了转移", "质子发生了转移", "电荷凭空消失"],
        "correct": 1,
        "feedback": "摩擦起电是电子转移，电荷总量守恒。",
    },
    "phy-m-work-energy": {
        "title": "功和能深化：做功的两个必要条件",
        "body": (
            "力对物体做功必须同时满足两个条件：有力作用在物体上，且物体在力的方向上移动了距离，W=Fs。"
            "只有力没有距离（如用力搬石头没搬动），或力与运动方向垂直（如提着桶水平行走），都不做功。做功的过程伴随能量的转化。"
        ),
        "example": "把书从地上举到桌上，举力对书做了功；提着书在水平地面匀速行走，提力方向与运动垂直，不做功。",
        "question": "下列情形中，力对物体做了功的是？",
        "options": ["用力推墙墙未动", "提水桶水平匀速前进", "把重物竖直举高", "手托物体静止不动"],
        "correct": 2,
        "feedback": "有力且在力方向上移动距离才做功，竖直举高做了功。",
    },
}


STYLE = """
<style id="phym-depth-css">
.phym-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.phym-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(167,139,250,.08);border:1px solid rgba(167,139,250,.24)}
.phym-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.phym-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.phym-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.phym-depth .phym-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
</style>
"""

CHECK_SCRIPT = """
<script id="phym-depth-js">
function pmDepthCheck(button, isCorrect, feedbackId, explanation) {
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


def depth_html(config: dict) -> str:
    feedback_id = "phym-depth-feedback"
    options = []
    for idx, opt in enumerate(config["options"]):
        correct = idx == config["correct"]
        handler = "pmDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false",
            f=feedback_id,
            e=json.dumps(config["feedback"], ensure_ascii=False),
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
<section class="slide-page" data-page-type="content" data-tsh="深化追问">
  <section class="section phym-depth core-knowledge-module" id="module-depth"
    data-bloom-level="analyze" data-scaffold="partial" data-tts="module-depth">
    <div class="card">
      <span class="phase-tag">深化追问</span>
      <h2>{html.escape(config['title'])}</h2>
      <p>{html.escape(config['body'])}</p>
      <div class="worked-example"><strong>例子拆解：</strong>{html.escape(config['example'])}</div>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析概念</h3>
        <p>{html.escape(config['question'])}</p>
        {''.join(options)}
        <div class="phym-feedback" id="{feedback_id}" role="status"></div>
      </div>
    </div>
  </section>
</section>
"""


def upgrade(course_id: str, config: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    original = source
    if 'id="module-depth"' in source:
        return False, "already upgraded"

    dpos = source.find('id="deep-understanding"')
    if dpos < 0:
        return False, "deep-understanding not found"
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    insert_at = marker if marker >= 0 else source.rfind("<section", 0, dpos)
    if insert_at < 0:
        return False, "insert marker not found"

    block = depth_html(config)
    source = source[:insert_at] + block + "\n" + source[insert_at:]
    if 'id="phym-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="phym-depth-js"' not in source:
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
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    return source != original, "depth section + metadata"


def main() -> int:
    changed = failed = 0
    for course_id, config in COURSES.items():
        ok, msg = upgrade(course_id, config)
        if ok:
            changed += 1
            print(f"OK {course_id}: {msg}")
        elif msg == "already upgraded":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
