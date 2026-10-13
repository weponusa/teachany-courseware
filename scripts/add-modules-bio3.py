#!/usr/bin/env python3
"""add-modules-bio3.py — 生物第 3 批：补写 worked-example 与 summary（人工撰写）"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

DATA = {
    "bio-circulation": [
        ("worked-example", "范例：为什么左心室的壁比右心室厚", [
            ("情境",
             "观察心脏结构图会发现，左心室的肌肉壁明显比右心室厚得多。"),
            ("分析",
             "左心室收缩时要把血液泵向全身各处（体循环），路程长、阻力大，"
             "需要更大的动力；右心室只需把血液泵到肺部（肺循环），"
             "路程短、阻力小。"),
            ("结论",
             "结构与功能相适应：需要产生更大压力的部位，肌肉壁就更发达。"
             "这也是判断心脏左右侧的依据之一。"),
        ]),
        ("summary", "小结：血液循环的途径", [
            ("血液成分",
             "血浆（运载血细胞、运输养料和废物）与血细胞："
             "红细胞运输氧、白细胞防御病菌、血小板止血凝血。"),
            ("心脏结构",
             "四个腔：左心房、左心室、右心房、右心室。"
             "房室瓣和动脉瓣保证血液只能单向流动，不会倒流。"),
            ("体循环",
             "左心室 → 主动脉 → 全身毛细血管 → 上、下腔静脉 → 右心房。"
             "血液由含氧丰富的动脉血变成含氧少的静脉血。"),
            ("肺循环",
             "右心室 → 肺动脉 → 肺部毛细血管 → 肺静脉 → 左心房。"
             "血液由静脉血变成动脉血。"),
            ("易错提醒",
             "区分动脉血与静脉血的依据是含氧量，不是血管名称——"
             "肺动脉里流的就是静脉血，肺静脉里流的是动脉血。"),
        ]),
    ],
    "bio-classification": [
        ("worked-example", "范例：给一只家猫定位它的七级「地址」", [
            ("情境",
             "生物分类体系有七个等级，试着给一只家猫找到它的位置。"),
            ("分析",
             "界：动物界（异养、大多能自由运动）；"
             "门：脊索动物门（有脊柱）；"
             "纲：哺乳纲（胎生哺乳、体表被毛）；"
             "目：食肉目（犬齿发达）；"
             "科：猫科（爪能伸缩）；"
             "属：猫属；种：猫。"),
            ("结论",
             "分类等级越高，包含的生物越多、共同特征越少；"
             "等级越低，包含的生物越少、共同特征越多。"
             "「种」是最基本的分类单位，同种生物亲缘关系最近。"),
        ]),
        ("summary", "小结：生物分类的等级与意义", [
            ("七个等级",
             "由大到小依次是：界、门、纲、目、科、属、种。"),
            ("规律",
             "等级越高，共同特征越少、亲缘关系越远；"
             "等级越低，共同特征越多、亲缘关系越近。"),
            ("种是最基本单位",
             "同种生物形态结构和生理功能相似，"
             "能相互交配并产生可育后代。"),
            ("分类依据",
             "主要根据形态结构、生理功能等特征的相似程度。"),
            ("意义",
             "便于识别和系统研究生物；弄清亲缘关系，"
             "才能为保护生物多样性制定针对性措施。"),
        ]),
    ],
    "bio-digestion": [
        ("worked-example", "范例：一粒米饭在消化道里的旅行", [
            ("情境",
             "跟随一粒米饭，看它经过哪些器官、发生什么变化。"),
            ("分析",
             "口腔：唾液淀粉酶把部分淀粉初步消化成麦芽糖"
             "（米饭嚼久了有甜味，就是这个原因）；"
             "胃：胃液中的胃蛋白酶初步消化蛋白质，食物变成食糜；"
             "小肠：肠液和胰液含多种消化酶，把淀粉分解为葡萄糖、"
             "蛋白质分解为氨基酸、脂肪分解为甘油和脂肪酸；"
             "大肠：吸收少量水、无机盐和部分维生素，残渣形成粪便。"),
            ("结论",
             "消化就是把大分子有机物分解成小分子。"
             "只有小分子物质才能穿过消化道壁被吸收进血液，"
             "因此小肠是消化和吸收的主要场所。"),
        ]),
        ("summary", "小结：消化系统的组成与功能", [
            ("消化道",
             "口腔 → 咽 → 食道 → 胃 → 小肠 → 大肠 → 肛门。"),
            ("消化腺",
             "唾液腺（唾液淀粉酶）、胃腺（胃蛋白酶）、"
             "肠腺和胰腺（多种消化酶）、肝脏（分泌胆汁，"
             "不含消化酶，能把脂肪乳化成微粒）。"),
            ("三大营养物质",
             "淀粉从口腔开始消化，蛋白质从胃开始消化，"
             "脂肪主要在小肠消化；三者最终都在小肠被彻底分解。"),
            ("小肠是主要场所的原因",
             "长约 5~6 米；内壁有皱襞和小肠绒毛，"
             "极大增加了吸收面积；绒毛壁薄，"
             "内有丰富的毛细血管和毛细淋巴管。"),
        ]),
    ],
}


def build(sid, title, blocks):
    parts = [f'\n<section class="section" id="{sid}" data-scaffold="full">',
             '<div class="card">',
             f'<h2 class="section-title">{escape(title)}</h2>']
    for head, body in blocks:
        if head == "范例":
            parts.append(f'<div class="worked-example"><strong>范例：</strong>{escape(body)}</div>')
        elif head == "易错提醒":
            parts.append(f'<p class="bioh-pitfall"><strong>易错提醒：</strong>{escape(body)}</p>')
        else:
            parts.append(f'<p><strong>{escape(head)}：</strong>{escape(body)}</p>')
    parts += ["</div></section>\n"]
    return "".join(parts)


def insert(html, sid, frag):
    after = {
        "worked-example": ["lesson-method", "lesson-focus", "deep-understanding"],
        "summary": ["posttest", "knowledge-graph"],
    }
    for a in after.get(sid, []):
        m = re.search(rf'<section\b[^>]*\bid="{a}"[^>]*>', html)
        if m:
            end = html.find("</section>", m.end())
            if end > 0:
                return html[:end + 10] + frag + html[end + 10:]
    m = re.search(r"\s*</body>", html)
    if m:
        return html[:m.start()] + frag + html[m.start():]
    return None


def main():
    dry = "--dry" in sys.argv
    n = 0
    for cid, mods in DATA.items():
        P = COMMUNITY / cid / "index.html"
        html = P.read_text(encoding="utf-8", errors="replace")
        for sid, title, blocks in mods:
            if re.search(rf'<section\b[^>]*\bid="{sid}"', html):
                print(f"  跳过（已有）{cid}/{sid}")
                continue
            new = insert(html, sid, build(sid, title, blocks))
            if new is None:
                print(f"  ⚠ 无插入点 {cid}/{sid}")
                continue
            html = new
            n += 1
        if not dry:
            P.write_text(html, encoding="utf-8")
    print(f"补写 {n} 个模块" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
