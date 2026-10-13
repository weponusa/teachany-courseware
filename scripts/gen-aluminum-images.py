#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 chem-h-aluminum-compounds 课件生成高质量 hero 图和插图。

方案：Pollinations 生成无文字底图 → Pillow 叠加中文文字标注 + 结构化布局 → WebP

5 张图：
  1. hero.png — 课件主题图（封面后，宽幅）
  2. al-reaction.png — 铝与酸碱反应（双路径对比）
  3. amphoteric.png — 氢氧化铝两性（中心辐射图）
  4. thermite.png — 铝热反应（反应流程）
  5. chem-h-aluminum-compounds-hero.png — 知识结构主图（信息密集型）
"""
import io
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

COURSE_DIR = Path(__file__).resolve().parent.parent / "community" / "chem-h-aluminum-compounds"
ASSETS_DIR = COURSE_DIR / "assets"

# ── 字体 ──
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


# ── 调色板 ──
C_BG_DARK = (10, 22, 40)        # 深蓝底
C_BG_MID = (20, 40, 70)         # 中蓝
C_ACCENT_BLUE = (56, 189, 248)  # 亮蓝
C_ACCENT_TEAL = (45, 212, 191)  # 青绿
C_ACCENT_PURPLE = (167, 139, 250)
C_ACCENT_GOLD = (251, 191, 36)
C_ACCENT_RED = (248, 113, 113)
C_ACCENT_GREEN = (74, 222, 128)
C_WHITE = (248, 250, 252)
C_DIM = (148, 163, 184)
C_CARD_BG = (15, 30, 55, 200)


def fetch_pollinations(prompt: str, w: int = 1024, h: int = 576, seed: int = 42) -> Image.Image | None:
    """从 Pollinations 获取底图。"""
    import urllib.parse
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={w}&height={h}&nologo=true&seed={seed}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
                return Image.open(io.BytesIO(data)).convert("RGBA")
        except Exception as e:
            print(f"  ⚠️ attempt {attempt+1}: {e}")
            time.sleep(3)
    return None


def make_gradient_bg(w, h, c1=C_BG_DARK, c2=C_BG_MID):
    """生成渐变背景。"""
    img = Image.new("RGBA", (w, h), c1)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


def draw_rounded_card(draw, xy, radius=16, fill=C_CARD_BG, outline=None, width=2):
    """绘制圆角卡片。"""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_text_with_shadow(draw, xy, text, font_obj, fill=C_WHITE, shadow=(0,0,0,160)):
    """带阴影文字。"""
    x, y = xy
    draw.text((x+2, y+2), text, font=font_obj, fill=shadow)
    draw.text((x, y), text, font=font_obj, fill=fill)


def add_decor_circles(img, draw):
    """添加装饰光圈。"""
    w, h = img.size
    # 右上角光圈
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([w-300, -100, w+100, 300], fill=(*C_ACCENT_BLUE, 25))
    od.ellipse([-100, h-250, 300, h+100], fill=(*C_ACCENT_PURPLE, 20))
    img.alpha_composite(overlay)


# ═══════════════════════════════════════════════
# 图1: hero.png — 课件主题图 (1280x720)
# ═══════════════════════════════════════════════
def gen_hero():
    print("🎨 [1/5] 生成 hero.png — 课件主题图...")
    W, H = 1280, 720
    bg = fetch_pollinations(
        "abstract chemistry background, aluminum element, molecular structures, "
        "blue teal gradient, clean modern flat design, no text no words",
        W, H, seed=101
    )
    if bg:
        bg = bg.resize((W, H))
        # 降低底图饱和度作为背景
        bg = bg.point(lambda p: int(p * 0.5))
    else:
        bg = make_gradient_bg(W, H)
    
    img = Image.new("RGBA", (W, H), C_BG_DARK)
    if bg:
        img.paste(bg, (0, 0))
    add_decor_circles(img, ImageDraw.Draw(img))
    draw = ImageDraw.Draw(img)

    # 标题
    draw_text_with_shadow(draw, (60, 50), "铝及其化合物", font(52, True), C_WHITE)
    # 副标题
    draw_text_with_shadow(draw, (60, 120), "地壳中含量最高的金属，拥有独特的「两面性」", font(26), C_ACCENT_BLUE)
    
    # 三个核心概念卡片
    cards = [
        ("⚛️ 铝单质", "银白色金属 · 密度2.70g/cm³\n表面致密Al₂O₃氧化膜保护", C_ACCENT_BLUE),
        ("⚖️ 两性", "Al₂O₃ + Al(OH)₃\n既能与酸反应，也能与碱反应", C_ACCENT_TEAL),
        ("🔥 铝热反应", "2Al + Fe₂O₃ → 2Fe + Al₂O₃\n高温放热，用于焊接金属", C_ACCENT_GOLD),
    ]
    card_w, card_h = 360, 200
    for i, (title, desc, color) in enumerate(cards):
        x = 60 + i * (card_w + 20)
        y = 300
        draw_rounded_card(draw, [x, y, x+card_w, y+card_h], radius=20,
                         fill=(15,30,55,210), outline=color, width=3)
        draw.text((x+24, y+20), title, font=font(28), fill=color)
        for j, line in enumerate(desc.split("\n")):
            draw.text((x+24, y+70+j*36), line, font=font(20), fill=C_WHITE)
    
    # 底部记忆锚点
    draw_rounded_card(draw, [60, 540, W-60, 620], radius=16,
                     fill=(5,15,30,200), outline=C_ACCENT_PURPLE, width=2)
    draw.text((90, 556), "💡 记忆锚点", font=font(22), fill=C_ACCENT_GOLD)
    draw.text((250, 556), "铝的活泼性 → 氧化膜保护 → 两性本质 → 铝热还原", font=font(22), fill=C_WHITE)
    
    # 页脚
    draw.text((60, 670), "TeachAny · 高中化学 · 铝及其化合物 · AI学伴/TTS/知识图谱", font=font(14), fill=C_DIM)
    
    save_webp(img, ASSETS_DIR / "hero.png")
    print("  ✅ hero.png 完成")


# ═══════════════════════════════════════════════
# 图2: al-reaction.png — 铝与酸碱反应 (1024x640)
# ═══════════════════════════════════════════════
def gen_al_reaction():
    print("🎨 [2/5] 生成 al-reaction.png — 铝与酸碱反应...")
    W, H = 1024, 640
    bg = fetch_pollinations(
        "chemistry reaction diagram, acid and base, test tubes, "
        "blue background, flat design, no text",
        W, H, seed=202
    )
    if bg:
        bg = bg.resize((W, H)).point(lambda p: int(p * 0.4))
    else:
        bg = make_gradient_bg(W, H)
    
    img = Image.new("RGBA", (W, H), C_BG_DARK)
    img.paste(bg, (0,0))
    add_decor_circles(img, ImageDraw.Draw(img))
    draw = ImageDraw.Draw(img)
    
    # 标题
    draw_text_with_shadow(draw, (40, 30), "铝与酸 / 碱反应对比", font(32), C_WHITE)
    
    # 左右两栏对比
    col_w = 440
    # 左栏：与酸反应
    x1 = 40
    draw_rounded_card(draw, [x1, 100, x1+col_w, 580], radius=18,
                     fill=(15,30,55,200), outline=C_ACCENT_BLUE, width=3)
    draw.text((x1+24, 120), "与酸反应（如HCl）", font=font(26), fill=C_ACCENT_BLUE)
    draw.text((x1+24, 165), "2Al + 6HCl → 2AlCl₃ + 3H₂↑", font=font(22), fill=C_WHITE)
    draw.text((x1+24, 205), "本质：Al 失电子，H⁺ 得电子", font=font(18), fill=C_DIM)
    # 特征列表
    features_acid = [
        "✓ 产生氢气（气泡）",
        "✓ 溶液变透明（AlCl₃可溶）",
        "✓ 与非氧化性酸反应",
        "✗ 冷浓HNO₃/H₂SO₄钝化",
    ]
    for i, f in enumerate(features_acid):
        color = C_ACCENT_GREEN if f.startswith("✓") else C_ACCENT_RED
        draw.text((x1+24, 260+i*40), f, font=font(20), fill=color)
    
    # 右栏：与碱反应
    x2 = 544
    draw_rounded_card(draw, [x2, 100, x2+col_w, 580], radius=18,
                     fill=(15,30,55,200), outline=C_ACCENT_TEAL, width=3)
    draw.text((x2+24, 120), "与强碱反应（如NaOH）", font=font(26), fill=C_ACCENT_TEAL)
    draw.text((x2+24, 165), "2Al + 2NaOH + 2H₂O → 2NaAlO₂ + 3H₂↑", font=font(20), fill=C_WHITE)
    draw.text((x2+24, 205), "本质：Al 两性，偏铝酸根生成", font=font(18), fill=C_DIM)
    features_base = [
        "✓ 同样产生氢气",
        "✓ 生成偏铝酸钠（NaAlO₂）",
        "✓ 只有强碱才反应",
        "💡 大多数金属不与碱反应",
    ]
    for i, f in enumerate(features_base):
        color = C_ACCENT_GREEN if "✓" in f else (C_ACCENT_GOLD if "💡" in f else C_ACCENT_RED)
        draw.text((x2+24, 260+i*40), f, font=font(20), fill=color)
    
    # 底部对比箭头
    draw.text((W//2-120, 595), "← 同：都产生H₂ ↑ →", font=font(18), fill=C_ACCENT_GOLD)
    
    save_webp(img, ASSETS_DIR / "al-reaction.png")
    print("  ✅ al-reaction.png 完成")


# ═══════════════════════════════════════════════
# 图3: amphoteric.png — 氢氧化铝两性 (1024x640)
# ═══════════════════════════════════════════════
def gen_amphoteric():
    print("🎨 [3/5] 生成 amphoteric.png — 氢氧化铝两性...")
    W, H = 1024, 640
    bg = fetch_pollinations(
        "molecular structure, amphoteric hydroxide, balance scale, "
        "chemistry diagram, blue purple gradient, flat design, no text",
        W, H, seed=303
    )
    if bg:
        bg = bg.resize((W, H)).point(lambda p: int(p * 0.4))
    else:
        bg = make_gradient_bg(W, H)
    
    img = Image.new("RGBA", (W, H), C_BG_DARK)
    img.paste(bg, (0,0))
    add_decor_circles(img, ImageDraw.Draw(img))
    draw = ImageDraw.Draw(img)
    
    draw_text_with_shadow(draw, (40, 30), "氢氧化铝 Al(OH)₃ 的两性", font(32), C_WHITE)
    draw.text((40, 75), "既能与酸反应，又能与强碱反应 → 两性氢氧化物", font=font(20), fill=C_DIM)
    
    # 中心 Al(OH)₃
    cx, cy = W//2, 320
    r = 80
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*C_ACCENT_PURPLE, 60), outline=C_ACCENT_PURPLE, width=4)
    draw.text((cx-65, cy-18), "Al(OH)₃", font=font(28), fill=C_WHITE)
    draw.text((cx-45, cy+15), "两性", font=font(18), fill=C_ACCENT_GOLD)
    
    # 左箭头：+酸
    draw.line([(cx-90, cy), (cx-280, cy)], fill=C_ACCENT_BLUE, width=4)
    draw.polygon([(cx-290, cy), (cx-270, cy-12), (cx-270, cy+12)], fill=C_ACCENT_BLUE)
    draw.text((cx-270, cy-50), "+ 酸 (HCl)", font=font(22), fill=C_ACCENT_BLUE)
    draw.text((cx-280, cy+20), "AlCl₃ + H₂O", font=font(18), fill=C_WHITE)
    
    # 左卡片
    draw_rounded_card(draw, [40, 420, 460, 590], radius=16,
                     fill=(15,30,55,200), outline=C_ACCENT_BLUE, width=2)
    draw.text((60, 440), "与酸反应 → 显碱性", font=font(22), fill=C_ACCENT_BLUE)
    draw.text((60, 478), "Al(OH)₃ + 3HCl → AlCl₃ + 3H₂O", font=font(18), fill=C_WHITE)
    draw.text((60, 510), "Al(OH)₃ 接受 H⁺，表现为碱", font=font(16), fill=C_DIM)
    draw.text((60, 540), "生成的 AlCl₃ 可溶于水", font=font(16), fill=C_DIM)
    
    # 右箭头：+碱
    draw.line([(cx+90, cy), (cx+280, cy)], fill=C_ACCENT_TEAL, width=4)
    draw.polygon([(cx+290, cy), (cx+270, cy-12), (cx+270, cy+12)], fill=C_ACCENT_TEAL)
    draw.text((cx+110, cy-50), "+ 强碱 (NaOH)", font=font(22), fill=C_ACCENT_TEAL)
    draw.text((cx+110, cy+20), "NaAlO₂ + H₂O", font=font(18), fill=C_WHITE)
    
    # 右卡片
    draw_rounded_card(draw, [564, 420, 984, 590], radius=16,
                     fill=(15,30,55,200), outline=C_ACCENT_TEAL, width=2)
    draw.text((584, 440), "与强碱反应 → 显酸性", font=font(22), fill=C_ACCENT_TEAL)
    draw.text((584, 478), "Al(OH)₃ + NaOH → NaAlO₂ + 2H₂O", font=font(18), fill=C_WHITE)
    draw.text((584, 510), "Al(OH)₃ 提供 H⁺，表现为酸", font=font(16), fill=C_DIM)
    draw.text((584, 540), "生成偏铝酸钠（需过量强碱）", font=font(16), fill=C_DIM)
    
    save_webp(img, ASSETS_DIR / "amphoteric.png")
    print("  ✅ amphoteric.png 完成")


# ═══════════════════════════════════════════════
# 图4: thermite.png — 铝热反应 (1024x640)
# ═══════════════════════════════════════════════
def gen_thermite():
    print("🎨 [4/5] 生成 thermite.png — 铝热反应...")
    W, H = 1024, 640
    bg = fetch_pollinations(
        "thermite reaction, sparks, molten iron, high temperature, "
        "industrial welding, orange glow, dark blue background, dramatic, no text",
        W, H, seed=404
    )
    if bg:
        bg = bg.resize((W, H)).point(lambda p: int(p * 0.4))
    else:
        bg = make_gradient_bg(W, H)
    
    img = Image.new("RGBA", (W, H), C_BG_DARK)
    img.paste(bg, (0,0))
    add_decor_circles(img, ImageDraw.Draw(img))
    draw = ImageDraw.Draw(img)
    
    draw_text_with_shadow(draw, (40, 30), "铝热反应 — 高温下的金属还原", font(32), C_WHITE)
    draw.text((40, 75), "铝粉与金属氧化物粉末混合 → 引燃 → 置换出金属", font=font(20), fill=C_DIM)
    
    # 反应方程式（核心）
    draw_rounded_card(draw, [40, 120, W-40, 220], radius=16,
                     fill=(5,15,30,220), outline=C_ACCENT_RED, width=3)
    draw.text((W//2-280, 140), "2Al + Fe₂O₃", font=font(32), fill=C_ACCENT_BLUE)
    draw.text((W//2-80, 148), "高温", font=font(18), fill=C_ACCENT_GOLD)
    draw.text((W//2-80, 175), "──→", font=font(22), fill=C_ACCENT_RED)
    draw.text((W//2+20, 140), "2Fe + Al₂O₃", font=font(32), fill=C_ACCENT_GOLD)
    draw.text((W//2-180, 190), "↑ 放出大量热（温度可达 2000°C+）", font=font(16), fill=C_DIM)
    
    # 三步流程
    steps = [
        ("① 引燃", "用镁条 + KClO₃\n作为引燃剂", C_ACCENT_GOLD),
        ("② 反应", "Al 还原 Fe₂O₃\n放出大量热", C_ACCENT_RED),
        ("③ 产物", "铁水沉底\nAl₂O₃ 渣浮上", C_ACCENT_TEAL),
    ]
    step_w = 280
    for i, (title, desc, color) in enumerate(steps):
        x = 60 + i * (step_w + 30)
        y = 260
        draw_rounded_card(draw, [x, y, x+step_w, y+180], radius=16,
                         fill=(15,30,55,200), outline=color, width=3)
        draw.text((x+20, y+20), title, font=font(28), fill=color)
        for j, line in enumerate(desc.split("\n")):
            draw.text((x+20, y+70+j*36), line, font=font(20), fill=C_WHITE)
        # 箭头连接
        if i < 2:
            ax = x + step_w + 5
            draw.line([(ax, y+90), (ax+20, y+90)], fill=C_DIM, width=3)
            draw.polygon([(ax+25, y+90), (ax+15, y+82), (ax+15, y+98)], fill=C_DIM)
    
    # 应用
    draw_rounded_card(draw, [40, 470, W-40, 600], radius=16,
                     fill=(5,15,30,200), outline=C_ACCENT_PURPLE, width=2)
    draw.text((60, 490), "🔧 实际应用", font=font(22), fill=C_ACCENT_PURPLE)
    apps = "焊接铁轨  ·  冶炼难熔金属（钒、铬、锰）  ·  定向燃烧焊接"
    draw.text((60, 530), apps, font=font(20), fill=C_WHITE)
    draw.text((60, 565), "💡 铝作为还原剂：对氧亲和力强，放热量大，经济安全", font=font(16), fill=C_ACCENT_GOLD)
    
    save_webp(img, ASSETS_DIR / "thermite.png")
    print("  ✅ thermite.png 完成")


# ═══════════════════════════════════════════════
# 图5: 知识结构主图 (1280x720)
# ═══════════════════════════════════════════════
def gen_knowledge_hero():
    print("🎨 [5/5] 生成 chem-h-aluminum-compounds-hero.png — 知识结构主图...")
    W, H = 1280, 720
    bg = fetch_pollinations(
        "knowledge graph structure, chemistry education, aluminum compounds, "
        "connected nodes, dark blue background, modern infographic, no text",
        W, H, seed=505
    )
    if bg:
        bg = bg.resize((W, H)).point(lambda p: int(p * 0.4))
    else:
        bg = make_gradient_bg(W, H)
    
    img = Image.new("RGBA", (W, H), C_BG_DARK)
    img.paste(bg, (0,0))
    add_decor_circles(img, ImageDraw.Draw(img))
    draw = ImageDraw.Draw(img)
    
    # 大标题
    draw_text_with_shadow(draw, (60, 40), "铝及其化合物 · 知识结构主图", font(44), C_WHITE)
    draw_text_with_shadow(draw, (60, 100), "为什么铝既能和酸反应，也能和强碱反应？", font(24), C_ACCENT_BLUE)
    
    # 中心问题框
    draw_rounded_card(draw, [W//2-250, 150, W//2+250, 210], radius=14,
                     fill=(*C_ACCENT_PURPLE, 40), outline=C_ACCENT_PURPLE, width=2)
    draw.text((W//2-220, 165), "核心问题：铝的「两面性」从何而来？", font=font(22), fill=C_ACCENT_PURPLE)
    
    # 三大模块（上排）
    modules = [
        ("核心机制", [
            "• Al 活泼金属 → 易失电子",
            "• 致密 Al₂O₃ 膜 → 抗腐蚀",
            "• Al₂O₃/Al(OH)₃ 两性",
        ], C_ACCENT_BLUE, 60),
        ("易错诊断", [
            "• 钝化 ≠ 不反应",
            "• 与碱反应需强碱",
            "• Al(OH)₃ 制取用铝盐+氨水",
        ], C_ACCENT_RED, 490),
        ("迁移应用", [
            "• 铝制餐具忌酸碱",
            "• 铝热反应焊接铁轨",
            "• 冶炼难熔金属",
        ], C_ACCENT_TEAL, 920),
    ]
    
    card_w, card_h = 300, 220
    for title, items, color, x in modules:
        draw_rounded_card(draw, [x, 250, x+card_w, 250+card_h], radius=18,
                         fill=(15,30,55,210), outline=color, width=3)
        draw.text((x+20, 270), title, font=font(28), fill=color)
        for j, item in enumerate(items):
            draw.text((x+20, 320+j*36), item, font=font(18), fill=C_WHITE)
    
    # 下排：反应链
    draw_rounded_card(draw, [60, 500, W-60, 620], radius=16,
                     fill=(5,15,30,200), outline=C_ACCENT_GOLD, width=2)
    draw.text((80, 515), "反应链", font=font(22), fill=C_ACCENT_GOLD)
    chain = "Al → Al₂O₃（氧化膜）→ AlCl₃（+酸）→ Al(OH)₃（+氨水）→ NaAlO₂（+强碱）"
    draw.text((80, 550), chain, font=font(20), fill=C_WHITE)
    draw.text((80, 585), "铝热：2Al + Fe₂O₃ →(高温) 2Fe + Al₂O₃", font=font(18), fill=C_ACCENT_TEAL)
    
    # 底部
    draw.text((60, 660), "TeachAny v7.x · 高中化学 · 铝及其化合物 · AI学伴 / TTS / 知识图谱 / Canvas互动",
              font=font(14), fill=C_DIM)
    
    save_webp(img, ASSETS_DIR / "chem-h-aluminum-compounds-hero.png")
    print("  ✅ chem-h-aluminum-compounds-hero.png 完成")


# ── 工具 ──
def save_webp(img: Image.Image, path: Path, quality=85):
    """保存为 PNG 格式（保持文件名兼容），内部用 WebP 编码优化大小。"""
    # 原图保持 PNG（文件名不变，HTML 引用不变）
    img_rgb = Image.new("RGB", img.size, C_BG_DARK)
    img_rgb.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
    img_rgb.save(str(path), "PNG", optimize=True)
    # 同时生成 WebP 版本
    webp_path = path.with_suffix(".webp")
    img_rgb.save(str(webp_path), "WEBP", quality=quality)
    sz_png = path.stat().st_size // 1024
    sz_webp = webp_path.stat().st_size // 1024
    print(f"  📦 {path.name}: PNG={sz_png}K, WebP={sz_webp}K")


def main():
    print("═══════════════════════════════════════════════")
    print("  铝及其化合物 — 高质量 hero 图 + 插图生成")
    print("  方案：Pollinations 底图 + Pillow 中文标注")
    print("═══════════════════════════════════════════════\n")
    
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    gen_hero()
    gen_al_reaction()
    gen_amphoteric()
    gen_thermite()
    gen_knowledge_hero()
    
    print("\n═══════════════════════════════════════════════")
    print("  ✅ 全部 5 张图生成完成")
    print(f"  输出目录: {ASSETS_DIR}")
    print("═══════════════════════════════════════════════")


if __name__ == "__main__":
    main()
