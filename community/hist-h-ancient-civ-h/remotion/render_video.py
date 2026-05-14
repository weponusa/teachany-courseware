#!/usr/bin/env python3
"""
古代亚非欧文明教学动画渲染脚本 v2.0
产出：1920x1080 @24fps MP4，含有意义的教学内容画面 + TTS语音

动画分 5 个 Beat（每 beat 约 8-10 秒）：
  Beat 1: 标题卡 + 大河文明主题引出
  Beat 2: 时间轴 — 四大文明依次出现（带年份标注）
  Beat 3: 古埃及聚焦（金字塔/象形文字/法老制度数据卡）
  Beat 4: 古巴比伦聚焦（汉谟拉比法典/楔形文字/六十进制）
  Beat 5: 四大文明对比总结表
"""
import os
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont

# ═══ 配置 ═══
WIDTH, HEIGHT = 1920, 1080
FPS = 24
FRAMES_DIR = "/tmp/ancient_civ_frames_v2"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = f"{BASE_DIR}/assets/video"
OUTPUT_FILE = f"{OUTPUT_DIR}/ancient-civ-evolution.mp4"
TTS_FILE = f"{BASE_DIR}/assets/tts/seg01_overview.mp3"

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ═══ 字体 ═══
def find_font(names, size):
    """按优先级查找可用字体"""
    import platform
    search_paths = []
    if platform.system() == 'Darwin':
        search_paths = ['/System/Library/Fonts', '/Library/Fonts',
                        os.path.expanduser('~/Library/Fonts')]
    else:
        search_paths = ['/usr/share/fonts', '/usr/local/share/fonts']

    for base in search_paths:
        for root, dirs, files in os.walk(base):
            for f in files:
                for name in names:
                    if name.lower() in f.lower() and f.endswith(('.ttf', '.ttc', '.otf')):
                        try:
                            return ImageFont.truetype(os.path.join(root, f), size)
                        except Exception:
                            continue
    # 兜底
    return ImageFont.load_default()

FONT_TITLE = find_font(['PingFang', 'STHeiti', 'Heiti', 'Source Han Sans'], 72)
FONT_SUBTITLE = find_font(['PingFang', 'STHeiti', 'Heiti', 'Source Han Sans'], 48)
FONT_BODY = find_font(['PingFang', 'STHeiti', 'Heiti', 'Source Han Sans'], 36)
FONT_SMALL = find_font(['PingFang', 'STHeiti', 'Heiti', 'Source Han Sans'], 28)
FONT_DATA = find_font(['PingFang', 'STHeiti', 'Heiti', 'Source Han Sans'], 32)

# ═══ 颜色方案 ═══
BG_DARK = (18, 24, 38)
BG_CARD = (30, 40, 60)
GOLD = (245, 178, 60)
BLUE = (59, 130, 246)
PURPLE = (139, 92, 246)
GREEN = (16, 185, 129)
RED = (239, 68, 68)
WHITE = (255, 255, 255)
DIM = (148, 163, 184)
SURFACE = (38, 50, 72)

# ═══ 文明数据 ═══
CIVS = [
    {"name": "古埃及", "year": "前3100年", "river": "尼罗河",
     "color": GOLD, "icon": "△",
     "achievements": ["金字塔建筑", "象形文字", "太阳历法", "木乃伊技术"],
     "data": {"持续": "3000年", "人口峰值": "500万", "文字符号": "700+"}},
    {"name": "古巴比伦", "year": "前3500年", "river": "两河流域",
     "color": BLUE, "icon": "⊞",
     "achievements": ["汉谟拉比法典", "楔形文字", "六十进制", "天文观测"],
     "data": {"法典条目": "282条", "数学": "60进制", "建筑": "空中花园"}},
    {"name": "古印度", "year": "前2500年", "river": "印度河",
     "color": PURPLE, "icon": "◎",
     "achievements": ["城市规划", "阿拉伯数字", "佛教", "种姓制度"],
     "data": {"城市面积": "260公顷", "发明": "零的概念", "宗教": "佛教/印度教"}},
    {"name": "古中国", "year": "前2070年", "river": "黄河长江",
     "color": GREEN, "icon": "鼎",
     "achievements": ["青铜器铸造", "甲骨文", "礼乐制度", "都江堰水利"],
     "data": {"朝代": "夏商周", "文字": "甲骨文", "技术": "青铜冶炼"}},
]

# ═══ 绘制辅助函数 ═══
def draw_rounded_rect(draw, xy, radius, fill, outline=None):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)

def draw_gradient_bg(img):
    """绘制从上到下的深色渐变背景"""
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(18 + (30 - 18) * t)
        g = int(24 + (40 - 24) * t)
        b = int(38 + (60 - 38) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return draw

def text_center_x(draw, text, font, y, fill=WHITE):
    """水平居中绘制文字"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)

def ease_out(t):
    return 1 - (1 - min(1, max(0, t))) ** 3

def ease_in_out(t):
    t = min(1, max(0, t))
    return 3*t*t - 2*t*t*t

# ═══ Beat 渲染函数 ═══

def render_beat1(progress):
    """Beat 1: 标题卡 — '古代亚非欧文明'"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = draw_gradient_bg(img)

    fade = ease_out(progress * 3)  # 前1/3时间淡入

    # 顶部装饰线
    line_w = int(400 * fade)
    cx = WIDTH // 2
    draw.line([(cx - line_w, 200), (cx + line_w, 200)], fill=GOLD, width=2)

    # 主标题
    if fade > 0.1:
        alpha_title = int(255 * min(1, fade))
        text_center_x(draw, "古代亚非欧文明", FONT_TITLE, 260, fill=(*WHITE[:3],))

    # 副标题
    sub_fade = ease_out(progress * 3 - 0.5)
    if sub_fade > 0:
        text_center_x(draw, "大河流域 · 文明摇篮 · 人类共同起源", FONT_SUBTITLE, 370, fill=DIM)

    # 四个文明缩略标记
    icon_fade = ease_out(progress * 2 - 0.6)
    if icon_fade > 0:
        positions = [(-300, GOLD, "古埃及"), (-100, BLUE, "古巴比伦"),
                     (100, PURPLE, "古印度"), (300, GREEN, "古中国")]
        for dx, color, name in positions:
            x = cx + dx
            y = 550
            # 圆点
            r = int(20 * icon_fade)
            draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=color)
            # 名字
            bbox = draw.textbbox((0, 0), name, font=FONT_SMALL)
            tw = bbox[2] - bbox[0]
            draw.text((x - tw//2, y + 30), name, font=FONT_SMALL, fill=color)

    # 底部提示
    hint_fade = ease_out(progress * 2 - 1.2)
    if hint_fade > 0:
        text_center_x(draw, "公元前 3500年 — 公元前 221年", FONT_BODY, 700, fill=(*DIM,))
        text_center_x(draw, "四大文明古国的诞生与辉煌", FONT_SMALL, 760, fill=DIM)

    return img


def render_beat2(progress):
    """Beat 2: 时间轴 — 四大文明依次浮现"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = draw_gradient_bg(img)

    # 标题
    draw.text((80, 50), "📅 文明诞生时间轴", font=FONT_SUBTITLE, fill=WHITE)

    # 时间轴线（水平）
    timeline_y = 300
    margin = 200
    draw.line([(margin, timeline_y), (WIDTH - margin, timeline_y)], fill=DIM, width=3)

    # 时间刻度
    years = [("前3500", 0.0), ("前3000", 0.15), ("前2500", 0.3),
             ("前2000", 0.5), ("前1500", 0.65), ("前1000", 0.8), ("前500", 1.0)]
    for label, pos in years:
        x = int(margin + (WIDTH - 2*margin) * pos)
        draw.line([(x, timeline_y - 10), (x, timeline_y + 10)], fill=DIM, width=2)
        bbox = draw.textbbox((0, 0), label, font=FONT_SMALL)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw//2, timeline_y + 20), label, font=FONT_SMALL, fill=DIM)

    # 四大文明按出现顺序浮现
    civ_positions = [
        (0.0, 0),    # 巴比伦 前3500
        (0.15, 1),   # 埃及 前3100 ≈ 0.12
        (0.3, 2),    # 印度 前2500
        (0.45, 3),   # 中国 前2070 ≈ 0.42
    ]
    # 调整 x 位置按年份
    year_pos = [0.0, 0.12, 0.3, 0.42]

    for i, (appear_threshold, civ_idx) in enumerate(civ_positions):
        civ = CIVS[civ_idx]
        local_fade = ease_out((progress - appear_threshold * 1.5) * 4)
        if local_fade <= 0:
            continue

        x = int(margin + (WIDTH - 2*margin) * year_pos[i])
        # 竖线指向
        line_end_y = timeline_y - 60 - i % 2 * 80
        draw.line([(x, timeline_y - 15), (x, line_end_y + 40)],
                  fill=civ["color"], width=3)

        # 文明卡片（浮现）
        card_w, card_h = 280, 160
        card_x = x - card_w // 2
        card_y = 450 + (i % 2) * 200
        offset_y = int(30 * (1 - local_fade))
        card_y += offset_y

        draw_rounded_rect(draw, (card_x, card_y, card_x + card_w, card_y + card_h),
                          radius=12, fill=SURFACE, outline=civ["color"])

        # 卡片内容
        draw.text((card_x + 20, card_y + 15), civ["name"], font=FONT_DATA, fill=civ["color"])
        draw.text((card_x + 20, card_y + 55), f"📍 {civ['river']}", font=FONT_SMALL, fill=WHITE)
        draw.text((card_x + 20, card_y + 90), f"🕐 {civ['year']}", font=FONT_SMALL, fill=DIM)
        draw.text((card_x + 20, card_y + 120), f"✦ {civ['achievements'][0]}", font=FONT_SMALL, fill=DIM)

        # 连接线
        draw.line([(x, line_end_y + 40), (x, card_y)], fill=civ["color"], width=2)

    return img


def render_beat3(progress):
    """Beat 3: 古埃及聚焦 — 数据卡"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = draw_gradient_bg(img)

    civ = CIVS[0]  # 古埃及

    # 左侧：标题和描述
    draw.text((80, 60), f"🏛️ {civ['name']}文明", font=FONT_TITLE, fill=civ["color"])
    draw.text((80, 160), f"尼罗河畔 · {civ['year']}统一 · 延续三千年", font=FONT_BODY, fill=DIM)

    # 成就列表（逐条浮现）
    draw.text((80, 250), "核心成就", font=FONT_SUBTITLE, fill=WHITE)
    for i, ach in enumerate(civ["achievements"]):
        item_fade = ease_out((progress - i * 0.15) * 5)
        if item_fade <= 0:
            continue
        y = 320 + i * 60
        # 圆点
        draw.ellipse([(90, y+12), (106, y+28)], fill=civ["color"])
        draw.text((120, y+5), ach, font=FONT_DATA, fill=WHITE)

    # 右侧：数据面板
    panel_fade = ease_out((progress - 0.3) * 3)
    if panel_fade > 0:
        panel_x = WIDTH // 2 + 100
        panel_y = 250
        panel_w = WIDTH - panel_x - 80
        panel_h = 400

        draw_rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                          radius=16, fill=SURFACE, outline=civ["color"])

        draw.text((panel_x + 30, panel_y + 20), "📊 关键数据", font=FONT_DATA, fill=civ["color"])

        data_items = [
            ("文明持续", "约 3000 年", "最长寿的古文明之一"),
            ("人口峰值", "约 500 万", "古代世界人口大国"),
            ("象形符号", "700+ 个", "比楔形文字更具图画性"),
            ("金字塔", "138 座", "人类最壮观的古代建筑"),
        ]
        for i, (label, value, note) in enumerate(data_items):
            item_y = panel_y + 80 + i * 80
            draw.text((panel_x + 30, item_y), label, font=FONT_SMALL, fill=DIM)
            draw.text((panel_x + 30, item_y + 30), value, font=FONT_DATA, fill=WHITE)
            draw.text((panel_x + 200, item_y + 35), note, font=FONT_SMALL, fill=DIM)

    # 底部时间线指示
    draw.text((80, HEIGHT - 80), "▶ 下一页：古巴比伦文明", font=FONT_SMALL, fill=DIM)

    return img


def render_beat4(progress):
    """Beat 4: 古巴比伦聚焦 — 数据卡"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = draw_gradient_bg(img)

    civ = CIVS[1]  # 古巴比伦

    # 标题
    draw.text((80, 60), f"📜 {civ['name']}文明", font=FONT_TITLE, fill=civ["color"])
    draw.text((80, 160), f"两河流域 · {civ['year']}文明萌芽 · 法律先驱", font=FONT_BODY, fill=DIM)

    # 成就列表
    draw.text((80, 250), "核心成就", font=FONT_SUBTITLE, fill=WHITE)
    for i, ach in enumerate(civ["achievements"]):
        item_fade = ease_out((progress - i * 0.15) * 5)
        if item_fade <= 0:
            continue
        y = 320 + i * 60
        draw.ellipse([(90, y+12), (106, y+28)], fill=civ["color"])
        draw.text((120, y+5), ach, font=FONT_DATA, fill=WHITE)

    # 右侧数据面板
    panel_fade = ease_out((progress - 0.3) * 3)
    if panel_fade > 0:
        panel_x = WIDTH // 2 + 100
        panel_y = 250
        panel_w = WIDTH - panel_x - 80
        panel_h = 400

        draw_rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                          radius=16, fill=SURFACE, outline=civ["color"])

        draw.text((panel_x + 30, panel_y + 20), "📊 关键数据", font=FONT_DATA, fill=civ["color"])

        data_items = [
            ("汉谟拉比法典", "282 条", "人类最早的成文法典"),
            ("数学体系", "六十进制", "影响今天的时间/角度"),
            ("文字系统", "楔形文字", "刻在泥板上的智慧"),
            ("天文成就", "星座命名", "将黄道分为12宫"),
        ]
        for i, (label, value, note) in enumerate(data_items):
            item_y = panel_y + 80 + i * 80
            draw.text((panel_x + 30, item_y), label, font=FONT_SMALL, fill=DIM)
            draw.text((panel_x + 30, item_y + 30), value, font=FONT_DATA, fill=WHITE)
            draw.text((panel_x + 200, item_y + 35), note, font=FONT_SMALL, fill=DIM)

    draw.text((80, HEIGHT - 80), "▶ 下一页：四大文明对比总结", font=FONT_SMALL, fill=DIM)

    return img


def render_beat5(progress):
    """Beat 5: 四大文明对比总结表"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = draw_gradient_bg(img)

    # 标题
    text_center_x(draw, "四大古文明对比", FONT_TITLE, 40, fill=WHITE)
    text_center_x(draw, "相同起源 · 独特贡献 · 相互影响", FONT_BODY, 130, fill=DIM)

    # 对比表格
    table_x = 100
    table_y = 200
    col_w = (WIDTH - 200) // 5
    row_h = 70

    # 表头
    headers = ["维度", "古埃及", "古巴比伦", "古印度", "古中国"]
    colors = [WHITE, GOLD, BLUE, PURPLE, GREEN]
    for i, (h, c) in enumerate(zip(headers, colors)):
        x = table_x + i * col_w
        draw.text((x + 10, table_y), h, font=FONT_DATA, fill=c)

    # 分隔线
    draw.line([(table_x, table_y + 50), (WIDTH - 100, table_y + 50)], fill=DIM, width=1)

    # 数据行
    rows = [
        ("大河", "尼罗河", "幼发拉底河", "印度河", "黄河长江"),
        ("文字", "象形文字", "楔形文字", "印章文字", "甲骨文"),
        ("政治", "法老专制", "城邦制", "种姓制度", "分封制"),
        ("宗教", "多神+来世", "多神教", "佛教/印度教", "祖先崇拜"),
        ("建筑", "金字塔", "塔庙/城墙", "浴场/排水", "宫殿/城墙"),
        ("科技", "太阳历/医学", "60进制/天文", "零/十进制", "青铜/水利"),
        ("法律", "死者之书", "汉谟拉比法典", "摩奴法典", "周礼/刑书"),
    ]

    for row_idx, row_data in enumerate(rows):
        row_fade = ease_out((progress - row_idx * 0.08) * 4)
        if row_fade <= 0:
            continue
        y = table_y + 65 + row_idx * row_h
        for col_idx, cell in enumerate(row_data):
            x = table_x + col_idx * col_w
            color = colors[col_idx] if col_idx > 0 else DIM
            draw.text((x + 10, y), cell, font=FONT_SMALL, fill=color)

    # 底部结论
    concl_fade = ease_out((progress - 0.7) * 4)
    if concl_fade > 0:
        text_center_x(draw, "🌍 四大文明：共同的大河起源，各自的辉煌贡献", FONT_BODY, HEIGHT - 100, fill=GOLD)

    return img


# ═══ 主渲染流程 ═══

# 每个 Beat 的时长（秒）
BEAT_DURATIONS = [9, 10, 9, 9, 8]  # 总计 45 秒
BEAT_RENDERERS = [render_beat1, render_beat2, render_beat3, render_beat4, render_beat5]

total_duration = sum(BEAT_DURATIONS)
total_frames = total_duration * FPS

print(f"═══ 古代亚非欧文明教学动画 v2.0 ═══")
print(f"分辨率: {WIDTH}x{HEIGHT} | FPS: {FPS} | 时长: {total_duration}s")
print(f"总帧数: {total_frames}")
print(f"Beat 分配: {BEAT_DURATIONS}")
print()

# 计算每个 beat 的起止帧
beat_ranges = []
frame_start = 0
for dur in BEAT_DURATIONS:
    frame_end = frame_start + dur * FPS
    beat_ranges.append((frame_start, frame_end))
    frame_start = frame_end

# 渲染每一帧（每 2 帧取 1 帧加速，ffmpeg 自动插值）
SKIP = 2
rendered = 0
for frame_idx in range(0, total_frames, SKIP):
    # 确定当前属于哪个 beat
    for beat_idx, (start, end) in enumerate(beat_ranges):
        if frame_idx < end:
            # 计算 beat 内进度 0~1
            beat_progress = (frame_idx - start) / (end - start)
            img = BEAT_RENDERERS[beat_idx](beat_progress)
            break
    else:
        img = BEAT_RENDERERS[-1](1.0)

    # 保存帧
    filename = f"{FRAMES_DIR}/frame_{frame_idx:05d}.png"
    img.save(filename, 'PNG')
    rendered += 1

    if rendered % 50 == 0:
        pct = frame_idx * 100 // total_frames
        print(f"  渲染进度: {rendered} 帧 ({pct}%)")

print(f"\n✅ 帧渲染完成: {rendered} 帧")
print("开始 ffmpeg 合成...")

# ffmpeg 合成（帧序列 + TTS 音频 → MP4）
cmd = [
    'ffmpeg', '-y',
    '-framerate', str(FPS // SKIP),
    '-pattern_type', 'glob',
    '-i', f'{FRAMES_DIR}/frame_*.png',
    '-i', TTS_FILE,
    '-vf', f'fps={FPS}',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
    '-c:a', 'aac', '-b:a', '128k',
    '-shortest',
    '-pix_fmt', 'yuv420p',
    OUTPUT_FILE
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    # 检查文件大小
    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"\n✅ 视频生成成功: {OUTPUT_FILE}")
    print(f"   文件大小: {size_mb:.1f} MB")

    # ffprobe 验证
    probe = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries',
         'stream=codec_type,codec_name,width,height,duration',
         '-print_format', 'json', OUTPUT_FILE],
        capture_output=True, text=True
    )
    import json
    info = json.loads(probe.stdout)
    for stream in info.get('streams', []):
        ct = stream['codec_type']
        cn = stream.get('codec_name', 'N/A')
        dur = stream.get('duration', 'N/A')
        if ct == 'video':
            w, h = stream.get('width', '?'), stream.get('height', '?')
            print(f"   视频轨: {cn} {w}x{h} ({dur}s)")
        else:
            print(f"   音频轨: {cn} ({dur}s)")
else:
    print(f"❌ ffmpeg 失败:")
    print(result.stderr[:800])

# 清理
subprocess.run(['rm', '-rf', FRAMES_DIR])
print("临时帧已清理")
