#!/usr/bin/env python3
"""为《红楼梦》课件生成 PNG 信息图（替代占位 SVG）。"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

FONT_FALLBACK = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]


def get_font(size: int = 24):
    for fp in FONT_FALLBACK:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill, outline=None):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)
    if outline:
        draw.line([x0 + radius, y0, x1 - radius, y0], fill=outline)
        draw.line([x0 + radius, y1, x1 - radius, y1], fill=outline)
        draw.line([x0, y0 + radius, x0, y1 - radius], fill=outline)
        draw.line([x1, y0 + radius, x1, y1 - radius], fill=outline)

# 红楼梦主题色
RB = {
    "bg": (18, 10, 13),
    "card": (45, 20, 28),
    "gold": (201, 162, 39),
    "rose": (251, 113, 133),
    "sky": (56, 189, 248),
    "mint": (34, 197, 94),
    "violet": (167, 139, 250),
    "text": (254, 243, 199),
    "text2": (231, 229, 228),
    "muted": (120, 113, 108),
}


def _header(draw, title: str, subtitle: str, w: int) -> None:
    draw.text((48, 36), title, font=get_font(40), fill=RB["text"])
    draw.text((48, 92), subtitle, font=get_font(22), fill=RB["text2"])
    draw.line([(48, 128), (w - 48, 128)], fill=RB["gold"], width=2)


def _three_cards(
    draw,
    items: list[tuple[str, str, str, tuple[int, int, int]]],
    y0: int,
    w: int,
    h: int,
) -> None:
    n = 3
    gap = 28
    card_w = (w - 96 - gap * (n - 1)) // n
    card_h = h - y0 - 120
    for i, (label, desc, _, color) in enumerate(items):
        x0 = 48 + i * (card_w + gap)
        draw_rounded_rect(draw, [x0, y0, x0 + card_w, y0 + card_h], 18, RB["card"], outline=color)
        draw.rectangle([x0, y0, x0 + card_w, y0 + 5], fill=color)
        draw.text((x0 + 20, y0 + 24), label, font=get_font(26), fill=color)
        line, lines = "", []
        for ch in desc:
            line += ch
            if len(line) >= max(12, card_w // 22):
                lines.append(line)
                line = ""
        if line:
            lines.append(line)
        for j, tl in enumerate(lines[:5]):
            draw.text((x0 + 20, y0 + 72 + j * 28), tl, font=get_font(18), fill=RB["text2"])


def gen_middle_hero(out: Path) -> None:
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), RB["bg"])
    draw = ImageDraw.Draw(img)
    draw.ellipse([900, -40, 1180, 240], fill=(201, 162, 39, 30))
    draw.ellipse([40, 480, 320, 760], fill=(167, 139, 250, 25))
    _header(
        draw,
        "《红楼梦》选读",
        "怎样用文本证据解释表达效果与思想情感？",
        w,
    )
    draw.text((48, 148), "角色：名著鉴赏员 · 初中语文 G9", font=get_font(20), fill=RB["muted"])
    _three_cards(
        draw,
        [
            ("人物关系", "先明确任务对象和文本范围，不能只凭印象回答。", "", RB["sky"]),
            ("细节伏笔", "拆成可标注的语言现象、结构关系和表达方法。", "", RB["violet"]),
            ("主题意蕴", "用原文词句与写作目的支撑判断，形成答题路径。", "", RB["mint"]),
        ],
        200,
        w,
        h,
    )
    draw_rounded_rect(draw, [48, 580, w - 48, 660], 16, (12, 7, 8), outline=RB["gold"])
    draw.text((72, 612), "记忆锚点：名著选读要从细节进入人物关系和主题意蕴。", font=get_font(22), fill=RB["gold"])
    draw.text((48, 688), "TeachAny · 初中语文 · AI 学伴 / TTS / 知识图谱", font=get_font(16), fill=RB["muted"])
    img.save(out, "PNG")


def gen_middle_concept(out: Path) -> None:
    w, h = 1200, 640
    img = Image.new("RGB", (w, h), RB["bg"])
    draw = ImageDraw.Draw(img)
    _header(draw, "《红楼梦》选读 · 概念结构图", "任务 → 证据 → 表达效果", w)
    _three_cards(
        draw,
        [
            ("人物关系", "把握人物处境与关系，为细节分析奠基。", "", RB["sky"]),
            ("细节伏笔", "关注词句、描写与结构中的关键信息。", "", RB["violet"]),
            ("主题意蕴", "回到思想情感与表达目的的概括。", "", RB["mint"]),
        ],
        160,
        w,
        h,
    )
    draw.text(
        (48, 560),
        "路径：从文本进入问题，再回到证据、方法、效果和表达。",
        font=get_font(22),
        fill=RB["gold"],
    )
    img.save(out, "PNG")


def gen_middle_process(out: Path) -> None:
    w, h = 1200, 640
    img = Image.new("RGB", (w, h), RB["bg"])
    draw = ImageDraw.Draw(img)
    _header(draw, "《红楼梦》选读 · 答题过程图", "圈画 → 判断 → 组织", w)
    steps = [
        ("① 圈画证据", "标出关键词句、描写与结构线索", RB["sky"]),
        ("② 判断方法", "说明用了什么写法、人物或结构手法", RB["violet"]),
        ("③ 组织答案", "证据 + 方法 + 效果 + 主旨", RB["mint"]),
    ]
    y0 = 180
    gap = 40
    box_w = (w - 96 - gap * 2) // 3
    for i, (title, desc, color) in enumerate(steps):
        x0 = 48 + i * (box_w + gap)
        draw_rounded_rect(draw, [x0, y0, x0 + box_w, y0 + 280], 18, RB["card"], outline=color)
        draw.text((x0 + 20, y0 + 28), title, font=get_font(24), fill=color)
        draw.text((x0 + 20, y0 + 90), desc, font=get_font(18), fill=RB["text2"])
        if i < 2:
            ax = x0 + box_w + 8
            draw.polygon([(ax, y0 + 140), (ax + 24, y0 + 128), (ax + 24, y0 + 152)], fill=RB["gold"])
    draw.text((48, 520), "名著选读：细节入手，证据说话，表达有据。", font=get_font(22), fill=RB["gold"])
    img.save(out, "PNG")


def gen_high_character_relations(out: Path) -> None:
    w, h = 960, 640
    img = Image.new("RGB", (w, h), RB["bg"])
    draw = ImageDraw.Draw(img)
    _header(draw, "贾府主要人物关系（简图）", "四大家族纽带 · 配合名场面精读", w)

    def node(cx, cy, text, fill, stroke):
        bw, bh = 140, 52
        draw_rounded_rect(draw, [cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2], 14, fill, outline=stroke)
        draw.text((cx, cy - 10), text, font=get_font(20), fill=RB["text"], anchor="mm")

    node(480, 110, "贾母", RB["card"], RB["gold"])
    node(260, 220, "贾政", (30, 58, 95), RB["sky"])
    node(700, 220, "王夫人", (30, 58, 95), RB["sky"])
    draw.line([(480, 136), (260, 194)], fill=RB["muted"], width=2)
    draw.line([(480, 136), (700, 194)], fill=RB["muted"], width=2)
    node(180, 360, "贾宝玉", (76, 5, 25), RB["rose"])
    node(480, 360, "林黛玉", (76, 5, 25), RB["rose"])
    node(760, 360, "薛宝钗", (66, 32, 6), RB["gold"])
    draw.line([(260, 246), (180, 334)], fill=RB["muted"], width=2)
    draw.line([(700, 246), (760, 334)], fill=RB["muted"], width=2)
    node(480, 470, "王熙凤（管家）", (49, 46, 129), RB["violet"])
    draw.line([(480, 136), (480, 444)], fill=RB["muted"], width=2)
    draw_rounded_rect(draw, [40, 530, w - 40, 610], 12, (12, 7, 8), outline=RB["muted"])
    draw.text(
        (56, 548),
        "宝玉—黛玉—宝钗构成爱情悲剧三角；凤姐联结权力与衰败。",
        font=get_font(16),
        fill=RB["text2"],
    )
    draw.text(
        (56, 578),
        "精读建议：葬花、挨打、抄检、好了歌。",
        font=get_font(16),
        fill=RB["muted"],
    )
    img.save(out, "PNG")


def gen_high_plot_timeline(out: Path) -> None:
    w, h = 960, 640
    img = Image.new("RGB", (w, h), RB["bg"])
    draw = ImageDraw.Draw(img)
    _header(draw, "《红楼梦》情节脉络", "通读 → 精读名场面 → 研讨收束", w)
    events = ["通读", "黛玉葬花", "宝玉挨打", "抄检大观园", "好了歌", "衰败收束"]
    y = 280
    draw.line([(80, y), (w - 80, y)], fill=RB["gold"], width=4)
    step = (w - 160) // (len(events) - 1)
    for i, ev in enumerate(events):
        x = 80 + i * step
        draw.ellipse([x - 10, y - 10, x + 10, y + 10], fill=RB["rose"])
        draw.text((x, y - 42), ev, font=get_font(18), fill=RB["text"], anchor="mm")
    draw.text(
        (48, 480),
        "沿时间轴把握家族兴衰，再回文本找细节证据。",
        font=get_font(20),
        fill=RB["gold"],
    )
    img.save(out, "PNG")


def gen_high_appreciation_lens(out: Path) -> None:
    w, h = 900, 500
    img = Image.new("RGB", (w, h), RB["bg"])
    draw = ImageDraw.Draw(img)
    _header(draw, "四层赏析透镜", "先圈原文，再选透镜，写效果，联系主旨", w)
    cx, cy, r = 450, 280, 160
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RB["muted"], width=2)
    draw.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=RB["card"], outline=RB["gold"], width=2)
    draw.text((cx, cy), "文本\n证据", font=get_font(18), fill=RB["text"], anchor="mm", align="center")
    lenses = [
        (0, -r - 30, "语言品味", RB["gold"]),
        (r + 50, 0, "人物形象", RB["rose"]),
        (0, r + 30, "结构照应", RB["sky"]),
        (-r - 80, 0, "主题意蕴", RB["mint"]),
    ]
    for dx, dy, label, color in lenses:
        draw.text((cx + dx, cy + dy), label, font=get_font(20), fill=color, anchor="mm")
    img.save(out, "PNG")


def gen_high_hero_infographic(out: Path) -> None:
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), RB["bg"])
    draw = ImageDraw.Draw(img)
    _header(draw, "《红楼梦》整本书阅读", "感动细节 → 四层赏析 → 研读研讨", w)
    draw.text((48, 148), "高中语文 G11 · chn-h-red-chamber", font=get_font(20), fill=RB["muted"])
    _three_cards(
        draw,
        [
            ("通读精读", "人物关系 · 情节时间轴", "", RB["gold"]),
            ("四层赏析", "名场面 · 批注实验", "", RB["rose"]),
            ("研讨追问", "小组论证", "", RB["sky"]),
        ],
        200,
        w,
        h,
    )
    draw_rounded_rect(draw, [48, 520, w - 520, 600], 16, (12, 7, 8), outline=RB["gold"])
    draw.text(
        (72, 548),
        "课标锚点：从最使自己感动的细节入手，反复品味、深入探究。",
        font=get_font(22),
        fill=RB["gold"],
    )
    draw_rounded_rect(draw, [w - 460, 520, w - 48, 600], 16, RB["card"], outline=RB["mint"])
    draw.text((w - 440, 548), "阅读档案：笔记 · 评介", font=get_font(22), fill=RB["mint"])
    img.save(out, "PNG")


JOBS = {
    "chn-m-dream-red-mansions": [
        ("hero-infographic.png", gen_middle_hero),
        ("concept-diagram.png", gen_middle_concept),
        ("process-diagram.png", gen_middle_process),
    ],
    "chn-h-red-chamber": [
        ("hero-infographic.png", gen_high_hero_infographic),
        ("character-relations.png", gen_high_character_relations),
        ("plot-timeline.png", gen_high_plot_timeline),
        ("appreciation-lens.png", gen_high_appreciation_lens),
    ],
}


def main() -> None:
    courses = sys.argv[1:] if len(sys.argv) > 1 else list(JOBS.keys())
    for cid in courses:
        if cid not in JOBS:
            print(f"⚠ 未知课件: {cid}")
            continue
        assets = ROOT / "community" / cid / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        print(f"📁 {cid}")
        for fname, fn in JOBS[cid]:
            out = assets / fname
            fn(out)
            print(f"  ✅ {fname} ({out.stat().st_size // 1024} KB)")
    print("完成")


if __name__ == "__main__":
    main()
