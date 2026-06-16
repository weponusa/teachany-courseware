#!/usr/bin/env python3
"""
批量升级推荐阅读（快乐读书吧）闯关游戏：
1. 为每个年级的每本推荐书创建独立闯关游戏
2. 调用 Agnes LLM 生成紧扣书籍内容的5关个性化题目
3. 调用 Agnes Image API 生成场景插画
4. 输出自包含 HTML 游戏文件
5. 更新 game-index.js

用法:
  python3 batch_reading_upgrade.py                      # 全量升级
  python3 batch_reading_upgrade.py --start 0 --count 5  # 从第0本开始，升级5本
  python3 batch_reading_upgrade.py --skip-images         # 跳过生图（只生成题目）
  python3 batch_reading_upgrade.py --resume              # 从上次断点继续
  python3 batch_reading_upgrade.py --dry-run             # 预览书目列表，不执行
"""

import json, os, sys, re, time, hashlib, argparse, traceback
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# ── 配置 ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
GAMES_DIR = BASE_DIR / "games" / "readings"
TEXTS_DIR = BASE_DIR / "texts"
BOOKS_DIR = TEXTS_DIR / "快乐读书吧"
ASSETS_DIR = BASE_DIR / "assets" / "generated-scenes"
INDEX_FILE = BASE_DIR / "data" / "game-index.js"
PROGRESS_FILE = BASE_DIR / "scripts" / ".reading_progress.json"

# LLM 配置 (Agnes)
LLM_API_KEY = "sk-sizYW5qbTggzJ2liRgzJ9wj7IYGajALpUBtvzOfY86h1BqRE"
LLM_BASE_URL = "https://apihub.agnes-ai.com/v1"
LLM_MODEL = "agnes-2.0-flash"

# Agnes 生图配置
AGNES_API_KEY = "sk-sizYW5qbTggzJ2liRgzJ9wj7IYGajALpUBtvzOfY86h1BqRE"
AGNES_BASE_URL = "https://apihub.agnes-ai.com/v1"
AGNES_MODEL = "agnes-image-2.1-flash"

# ── 推荐书目完整列表 ──────────────────────────────────────────────────
# 结构: (grade, volume, book_title, author, genre, brief, text_source)
#   text_source: "book:文件名" 表示从快乐读书吧目录取整本书
#                "grade:文件名" 表示从年级文件夹取对应课文
#                "none" 表示无本地文本，用LLM知识生成

READING_BOOKS = [
    # ── 一年级上册：和大人一起读 ──
    (1, "上册", "小兔子乖乖", "", "童谣儿歌",
     "经典童谣，讲述小兔子不给大灰狼开门的故事，教会孩子安全意识",
     "none"),
    (1, "上册", "剪窗花", "", "童谣儿歌",
     "描写过年剪窗花的欢快童谣，展现传统民俗文化之美",
     "none"),
    (1, "上册", "小松鼠找花生", "", "童话故事",
     "小松鼠等了一秋天却没找到花生果，原来花生果长在地下",
     "none"),
    (1, "上册", "拔萝卜", "", "童话故事",
     "老公公拔萝卜拔不动，全家齐心协力终于拔出大萝卜",
     "none"),

    # ── 一年级下册：读读童谣和儿歌 ──
    (1, "下册", "摇摇船", "", "童谣儿歌",
     "经典摇篮曲童谣，充满韵律美和童趣",
     "none"),
    (1, "下册", "小刺猬理发", "鲁兵", "儿歌",
     "小刺猬去理发店理发的趣味儿歌，语言活泼，想象丰富",
     "none"),
    (1, "下册", "阳光", "", "童谣儿歌",
     "描写阳光温暖万物的优美童谣，让孩子感受大自然的美好",
     "none"),
    (1, "下册", "谁会飞", "", "童谣儿歌",
     "问答式儿歌，让孩子认识各种动物的本领",
     "none"),

    # ── 二年级上册：读读童话故事 ──
    (2, "上册", "小鲤鱼跳龙门", "金近", "童话故事",
     "小鲤鱼们勇敢地跳过龙门，实现了自己的梦想",
     "none"),
    (2, "上册", "孤独的小螃蟹", "冰波", "童话故事",
     "小螃蟹的朋友小青蟹走了，它在等待中帮助了很多小动物",
     "none"),
    (2, "上册", "小狗的小房子", "孙幼军", "童话故事",
     "小狗带着小房子去找小猫玩，一路上发生了许多有趣的事",
     "none"),
    (2, "上册", "一只想飞的猫", "陈伯吹", "童话故事",
     "一只骄傲的猫总想飞上天，结果摔了大跟头，学会了谦虚",
     "none"),
    (2, "上册", "歪脑袋木头桩", "严文井", "童话故事",
     "一个歪着脑袋的木头桩瞧不起大家，最后认识到自己的错误",
     "none"),

    # ── 二年级下册：读读儿童故事 ──
    (2, "下册", "神笔马良", "洪汛涛", "民间故事",
     "穷孩子马良得到一支神笔，画什么就变成什么，帮助穷人",
     "none"),
    (2, "下册", "七色花", "卡塔耶夫", "童话故事",
     "小女孩珍妮得到一朵七色花，每片花瓣能实现一个愿望",
     "none"),
    (2, "下册", "大头儿子和小头爸爸", "郑春华", "儿童故事",
     "大头儿子和小头爸爸之间充满温情的日常生活故事",
     "none"),
    (2, "下册", "愿望的实现", "泰戈尔", "儿童故事",
     "父子互换身份后才体会到对方的不易，学会互相理解",
     "none"),

    # ── 三年级上册：在那奇妙的王国里 ──
    (3, "上册", "卖火柴的小女孩", "安徒生", "童话",
     "大年夜，一个卖火柴的小女孩在寒冷中点燃火柴，看到了美好的幻象",
     "book:安徒生童话.txt"),
    (3, "上册", "丑小鸭", "安徒生", "童话",
     "一只被嘲笑的丑小鸭经历磨难，最终变成了美丽的白天鹅",
     "book:安徒生童话.txt"),
    (3, "上册", "拇指姑娘", "安徒生", "童话",
     "拇指姑娘只有拇指大小，经历了许多冒险最终找到了幸福",
     "book:安徒生童话.txt"),
    (3, "上册", "稻草人", "叶圣陶", "童话",
     "稻草人看到田野里发生的一切，同情苦难的人们却无能为力",
     "none"),
    (3, "上册", "灰姑娘", "格林兄弟", "童话",
     "善良的灰姑娘在仙女帮助下参加舞会，最终与王子幸福生活",
     "book:格林童话.txt"),

    # ── 三年级下册：小故事大道理 ──
    (3, "下册", "叶公好龙", "", "寓言",
     "叶公说自己喜欢龙，真龙来了他却吓得要命。讽刺口是心非的人",
     "none"),
    (3, "下册", "狐狸和葡萄", "伊索", "寓言",
     "狐狸吃不到葡萄就说葡萄是酸的，讽刺自欺欺人的心态",
     "book:伊索寓言.txt"),
    (3, "下册", "龟兔赛跑", "伊索", "寓言",
     "骄傲的兔子在比赛中睡觉，坚持不懈的乌龟反而赢了比赛",
     "book:伊索寓言.txt"),
    (3, "下册", "守株待兔", "", "寓言",
     "农夫等着兔子再撞到树桩上，结果庄稼荒废了。告诫人们不要指望不劳而获",
     "none"),
    (3, "下册", "自相矛盾", "", "寓言",
     "一个人同时夸自己的矛和盾天下无敌，自相矛盾让人发笑",
     "none"),

    # ── 四年级上册：很久很久以前 ──
    (4, "上册", "盘古开天地", "", "神话",
     "盘古用大斧头劈开天和地，用自己的身体化为万物",
     "none"),
    (4, "上册", "女娲补天", "", "神话",
     "天塌了一个大窟窿，女娲炼五色石补天，拯救了苍生",
     "none"),
    (4, "上册", "精卫填海", "", "神话",
     "炎帝的小女儿被大海淹没后化为精卫鸟，每天衔石子填海",
     "none"),
    (4, "上册", "普罗米修斯", "", "神话",
     "普罗米修斯为人类盗取天火，被宙斯锁在高加索山受罚",
     "none"),

    # ── 四年级下册：十万个为什么 ──
    (4, "下册", "十万个为什么", "米·伊林", "科普",
     "从穿衣吃饭到自然现象，用有趣的方式解答孩子的十万个为什么",
     "none"),
    (4, "下册", "看看我们的地球", "李四光", "科普",
     "著名地质学家李四光讲述地球的奥秘，从地壳运动到矿产资源",
     "none"),
    (4, "下册", "灰尘的旅行", "高士其", "科普",
     "跟随灰尘去旅行，了解灰尘从哪里来、到哪里去",
     "none"),
    (4, "下册", "人类起源的演化过程", "贾兰坡", "科普",
     "从猿到人的漫长进化之路，探索人类的起源和发展",
     "none"),

    # ── 五年级上册：从前有座山 ──
    (5, "上册", "田螺姑娘", "", "民间故事",
     "善良的农夫捡到一个大田螺，原来是田螺姑娘在暗中帮他做家务",
     "none"),
    (5, "上册", "梁山伯与祝英台", "", "民间故事",
     "梁山伯与祝英台同窗三年结下深厚友情，最终化蝶双飞",
     "none"),
    (5, "上册", "猎人海力布", "", "民间故事",
     "海力布为了救乡亲们说出了秘密，自己变成了石头",
     "none"),
    (5, "上册", "列那狐的故事", "", "民间故事",
     "聪明狡猾的狐狸列那用智慧一次次戏弄强大的对手",
     "none"),

    # ── 五年级下册：读古典名著 ──
    (5, "下册", "西游记", "吴承恩", "古典名著",
     "唐僧师徒四人西天取经，历经九九八十一难终成正果",
     "book:西游记.txt"),
    (5, "下册", "三国演义", "罗贯中", "古典名著",
     "东汉末年群雄割据，魏蜀吴三国鼎立的英雄传奇",
     "book:三国演义.txt"),
    (5, "下册", "水浒传", "施耐庵", "古典名著",
     "一百零八位好汉被逼上梁山替天行道的传奇故事",
     "book:水浒传.txt"),
    (5, "下册", "红楼梦", "曹雪芹", "古典名著",
     "贾宝玉、林黛玉、薛宝钗的爱情悲剧与贾府的兴衰",
     "book:红楼梦.txt"),

    # ── 六年级上册：笑与泪，经历与成长 ──
    (6, "上册", "童年", "高尔基", "成长小说",
     "阿廖沙在外祖父家经历了苦难的童年，却始终保持善良",
     "none"),
    (6, "上册", "小英雄雨来", "管桦", "成长小说",
     "抗日战争中，12岁的雨来机智勇敢保护交通员的故事",
     "none"),
    (6, "上册", "爱的教育", "亚米契斯", "成长小说",
     "意大利小男孩安利柯的日记，记录了同学、老师和父母之间的爱",
     "none"),

    # ── 六年级下册：漫步世界名著花园 ──
    (6, "下册", "鲁滨逊漂流记", "笛福", "世界名著",
     "鲁滨逊流落荒岛28年，靠智慧和勇气生存下来",
     "none"),
    (6, "下册", "骑鹅旅行记", "拉格洛夫", "世界名著",
     "淘气的尼尔斯骑在鹅背上跟随大雁飞过瑞典全境",
     "none"),
    (6, "下册", "汤姆·索亚历险记", "马克·吐温", "世界名著",
     "汤姆·索亚和伙伴们在密西西比河畔的冒险故事",
     "none"),
    (6, "下册", "爱丽丝漫游奇境", "刘易斯·卡罗尔", "世界名著",
     "爱丽丝掉进兔子洞后进入一个荒诞奇妙的奇境世界",
     "none"),
]


# ── 工具函数 ────────────────────────────────────────────────────────────

def api_call(url, data, api_key, max_retries=3):
    """通用 API 调用，带重试"""
    payload = json.dumps(data).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://magic-reading-academy.local",
        "X-Title": "Magic Reading Academy",
    }
    for attempt in range(max_retries):
        try:
            req = Request(url, data=payload, headers=headers, method="POST")
            with urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (HTTPError, URLError, Exception) as e:
            print(f"  ⚠️  API 调用失败 (第{attempt+1}次): {e}")
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 10
                print(f"  ⏳ 等待 {wait}s 后重试...")
                time.sleep(wait)
            else:
                raise


def make_book_id(grade, volume, title):
    """生成书目唯一ID，如 g3-a-rb05"""
    vol_letter = "a" if volume == "上册" else "b"
    # 用 title 的 md5 前6位确保唯一
    title_hash = hashlib.md5(title.encode()).hexdigest()[:6]
    return f"g{grade}-{vol_letter}-rb{title_hash}"


def make_html_filename(book_id):
    """生成 HTML 文件名"""
    return f"{book_id}.html"


def extract_book_excerpt(book_file, target_title, max_chars=3000):
    """从整本书中提取与目标故事相关的章节片段"""
    if not book_file.exists():
        return None

    text = book_file.read_text(encoding="utf-8", errors="ignore")

    # 清理HTML标签
    text = re.sub(r'<[^>]+>', '', text)

    # 根据书名和故事名定位相关章节
    # 安徒生童话/格林童话/伊索寓言：按故事标题查找
    title_clean = target_title.replace("·", "").replace("（", "").replace("）", "")

    # 尝试精确匹配故事标题
    patterns = [
        rf'{re.escape(title_clean)}',
        rf'(?:^|\n)\s*{re.escape(title_clean)}\s*(?:\n|$)',
    ]

    best_pos = -1
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            best_pos = m.start()
            break

    if best_pos >= 0:
        # 从匹配位置开始截取
        excerpt = text[best_pos:best_pos + max_chars]
        return excerpt.strip()

    # 如果找不到精确匹配，取前3000字（包含简介）
    # 跳过版权声明等前置信息
    start = text.find("========正文========")
    if start < 0:
        start = text.find("第一回") or 0
    if start < 0:
        start = 500  # 跳过开头的版权声明

    excerpt = text[start:start + max_chars]
    return excerpt.strip()


def get_book_text(book_entry):
    """获取书籍的文本内容用于出题"""
    grade, volume, title, author, genre, brief, text_source = book_entry

    if text_source == "none":
        # 没有本地文本，返回简介（LLM用通用知识出题）
        return brief

    if text_source.startswith("book:"):
        filename = text_source[5:]
        book_path = BOOKS_DIR / filename
        excerpt = extract_book_excerpt(book_path, title)
        if excerpt and len(excerpt) > 50:
            return excerpt
        return brief

    if text_source.startswith("grade:"):
        filename = text_source[6:]
        grade_map = {
            (1, "上册"): "一上", (1, "下册"): "一下",
            (2, "上册"): "二上", (2, "下册"): "二下",
            (3, "上册"): "三上", (3, "下册"): "三下",
            (4, "上册"): "四上", (4, "下册"): "四下",
            (5, "上册"): "五上", (5, "下册"): "五下",
            (6, "上册"): "六上", (6, "下册"): "六下",
        }
        folder = grade_map.get((grade, volume), "")
        if folder:
            filepath = TEXTS_DIR / folder / filename
            if filepath.exists():
                text = filepath.read_text(encoding="utf-8")
                # 简单提取
                if len(text) > 3000:
                    text = text[:3000]
                return text
    return brief


# ── LLM 生成题目 ────────────────────────────────────────────────────────

def generate_levels_for_book(book_entry, text_content):
    """调用 LLM 为推荐书籍生成 5 关个性化题目"""
    grade, volume, title, author, genre, brief, _ = book_entry

    # 根据年级调整提示
    if grade <= 2:
        grade_hint = "1-2年级低年级学生，题目要简单直白，用词浅显，选项简短（每项不超过15字），故事叙述要活泼可爱。"
    elif grade <= 4:
        grade_hint = "3-4年级中年级学生，可以考查理解、推理和写作手法，选项可以稍长（每项不超过25字），故事叙述要有趣味性。"
    else:
        grade_hint = "5-6年级高年级学生，可以考查深层理解、修辞手法、主题思想、作者意图，选项可以有一定深度（每项不超过30字）。"

    author_info = f"，作者：{author}" if author else ""
    text_section = f"\n\n【参考文本片段】\n{text_content[:2500]}" if len(text_content) > 100 else ""

    prompt = f"""你是一位优秀的小学语文教师，擅长设计互动闯关游戏。

请为推荐阅读书目《{title}》（{genre}{author_info}）设计5关闯关题目。

【书籍简介】
{brief}
{text_section}

【学生年级】{grade}年级
{grade_hint}

【输出要求】
请严格输出以下JSON格式（不要输出任何其他文字），5个关卡对象组成的数组：

```json
[
  {{
    "tag": "第 1 关 · 场景小标题",
    "img": "英文图像提示词，描述该关卡的场景画面，children picture book style, warm colors, no text",
    "story": "该关卡的场景叙述（50-80字），引用或改编书中的情节，让学生代入情境",
    "q": "紧扣书籍内容的选择题（不超过25字）",
    "hint": "简短提示（不超过20字）",
    "opts": [
      {{"t": "正确选项", "c": true}},
      {{"t": "干扰项1", "c": false}},
      {{"t": "干扰项2", "c": false}},
      {{"t": "干扰项3", "c": false}}
    ],
    "fb": "答题反馈（30-60字），解释为什么正确，联系书籍内容"
  }}
]
```

【设计要求】
1. 每关的问题必须紧扣《{title}》的具体内容（人物、情节、寓意、细节等）
2. 5关要覆盖书籍的不同方面，形成层层递进：
   第1关：故事背景/人物介绍
   第2关：关键情节理解
   第3关：重要细节/词句理解
   第4关：深层含义/写作手法
   第5关：主题感悟/延伸思考
3. story（场景叙述）要生动有趣，让学生有代入感
4. img（图像提示词）必须用英文，描述书中具体场景画面
5. 正确答案必须准确无误，符合原著内容
6. 干扰项要有迷惑性但明显不符合书籍内容

请直接输出JSON数组，不要有任何前缀或后缀文字。"""

    data = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "你是小学语文教学专家，只输出JSON，不输出任何其他内容。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
    }

    result = api_call(f"{LLM_BASE_URL}/chat/completions", data, LLM_API_KEY)
    content = result["choices"][0]["message"]["content"].strip()

    # 提取 JSON
    m = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', content, re.DOTALL)
    if m:
        content = m.group(1)
    else:
        content = content.strip()
        if not content.startswith("["):
            start = content.find("[")
            end = content.rfind("]")
            if start >= 0 and end > start:
                content = content[start:end+1]

    levels = json.loads(content)
    assert isinstance(levels, list) and len(levels) == 5, f"期望5关，实际{len(levels)}关"

    # 验证每关结构
    for i, lv in enumerate(levels):
        assert "tag" in lv, f"第{i+1}关缺少tag"
        assert "q" in lv, f"第{i+1}关缺少q"
        assert "opts" in lv and len(lv["opts"]) == 4, f"第{i+1}关选项数不是4"
        correct_count = sum(1 for o in lv["opts"] if o.get("c"))
        assert correct_count == 1, f"第{i+1}关正确答案数={correct_count}，应为1"

    return levels


# ── Agnes 生图 ──────────────────────────────────────────────────────────

def generate_image(prompt, save_path, max_retries=3):
    """调用 Agnes API 生成图片并保存到本地"""
    final_prompt = prompt + ", children storybook illustration, warm lighting, suitable for elementary school students, no text, high quality"

    data = {
        "model": AGNES_MODEL,
        "prompt": final_prompt,
        "n": 1,
        "size": "1024x1024",
    }

    result = api_call(f"{AGNES_BASE_URL}/images/generations", data, AGNES_API_KEY, max_retries)
    item = result.get("data", [{}])[0]

    if item.get("url"):
        req = Request(item["url"])
        with urlopen(req, timeout=60) as resp:
            img_data = resp.read()
    elif item.get("b64_json"):
        import base64
        img_data = base64.b64decode(item["b64_json"])
    else:
        raise ValueError("Agnes API 返回为空")

    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(img_data)
    return save_path


# ── HTML 模板 ────────────────────────────────────────────────────────────

HTML_TEMPLATE = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}互动挑战</title>
<style>
:root{{--bg:#0f1022;--panel:#1b1d3d;--panel2:#242752;--gold:#e7c66b;--ink:#f8f0d8;--muted:#c4bddb;--line:rgba(231,198,107,.24);--ok:#62d99a;--no:#e98175}}
*{{box-sizing:border-box}}html,body{{margin:0}}body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:radial-gradient(1000px 540px at 50% -10%,#34466f 0%,transparent 62%),radial-gradient(900px 520px at 100% 100%,#253d34 0%,transparent 55%),var(--bg);color:var(--ink);min-height:100vh}}.stars{{position:fixed;inset:0;pointer-events:none;opacity:.42}}.wrap{{position:relative;z-index:1;max-width:840px;margin:0 auto;padding:18px 16px 58px}}.top{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}.crest{{width:48px;height:48px;border-radius:14px;background:linear-gradient(160deg,#263a52,#546b4a);border:1px solid var(--line);display:grid;place-items:center;color:var(--gold);font-weight:900}}.title h1{{font-size:19px;margin:0}}.title p{{margin:3px 0 0;font-size:12px;color:var(--muted)}}.badge{{margin-left:auto;font-size:12px;color:var(--gold);background:rgba(231,198,107,.1);border:1px solid var(--line);border-radius:999px;padding:6px 12px}}.steps{{display:flex;gap:6px;margin:0 0 16px}}.step{{flex:1;height:6px;border-radius:999px;background:rgba(255,255,255,.08)}}.step.done{{background:var(--gold)}}.step.cur{{background:linear-gradient(90deg,var(--gold),rgba(231,198,107,.2))}}.card{{background:linear-gradient(180deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:0 22px 56px rgba(0,0,0,.34)}}.scene-tag{{display:inline-block;font-size:12px;color:var(--gold);background:rgba(231,198,107,.1);border:1px solid var(--line);border-radius:999px;padding:5px 12px;margin-bottom:14px}}.stage{{position:relative;width:100%;aspect-ratio:16/10;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#111831;margin-bottom:15px}}.stage img{{width:100%;height:100%;object-fit:cover;display:block}}.stage .loading{{position:absolute;inset:0;display:grid;place-items:center;color:var(--muted);background:linear-gradient(135deg,rgba(255,255,255,.04),rgba(0,0,0,.18));text-align:center;padding:20px}}.story{{font-size:15px;line-height:1.9;margin:0 0 12px}}.story em{{font-style:normal;color:var(--gold)}}.qbox{{margin-top:16px;padding-top:16px;border-top:1px dashed var(--line)}}.q{{font-size:18px;font-weight:800;line-height:1.65;margin:0 0 4px}}.hint{{font-size:12px;color:var(--muted);margin:0 0 12px}}.opts{{display:grid;gap:10px}}.opt{{text-align:left;font-size:14px;line-height:1.55;padding:14px 15px;border-radius:14px;border:1px solid var(--line);background:rgba(255,255,255,.04);color:var(--ink);cursor:pointer;font-family:inherit}}.opt:hover{{border-color:var(--gold);background:rgba(231,198,107,.08)}}.opt.ok{{border-color:var(--ok);background:rgba(98,217,154,.14);color:#c8f7df}}.opt.no{{border-color:var(--no);background:rgba(233,129,117,.14);color:#ffd0ca}}.feedback{{display:none;margin-top:14px;padding:14px 15px;border-radius:14px;font-size:13px;line-height:1.8;border:1px solid var(--line);background:rgba(231,198,107,.07)}}.feedback.show{{display:block}}.nav{{display:flex;gap:10px;margin-top:16px}}button{{font-family:inherit}}.btn{{flex:1;border:0;border-radius:14px;padding:13px;font-size:14px;font-weight:800;cursor:pointer}}.btn-primary{{background:linear-gradient(180deg,var(--gold),#bd9343);color:#241b08}}.btn-primary:disabled{{opacity:.45;cursor:default}}.btn-ghost{{background:rgba(255,255,255,.06);color:var(--muted);border:1px solid var(--line)}}.end{{text-align:center;padding:10px 0}}.end h2{{color:var(--gold);font-size:26px;margin:8px 0}}.blurb{{font-size:15px;line-height:1.9;color:var(--ink)}}.create{{margin-top:18px;text-align:left;border:1px solid var(--line);border-radius:18px;padding:16px;background:rgba(255,255,255,.05)}}.create h3{{margin:0 0 8px;color:var(--gold)}}.create p{{margin:0 0 12px;color:var(--muted);line-height:1.75;font-size:13px}}.prompt-row{{display:flex;gap:8px}}.prompt-row input{{flex:1;border:1px solid var(--line);border-radius:12px;background:rgba(0,0,0,.22);color:var(--ink);padding:12px;font:inherit}}.image-box{{display:none;margin-top:14px;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#111}}.image-box img{{display:block;width:100%;height:auto}}.image-caption{{padding:10px 12px;color:var(--muted);font-size:12px;line-height:1.6}}@media(max-width:640px){{.wrap{{padding:12px 10px 42px}}.card{{padding:16px;border-radius:16px}}.prompt-row{{display:grid}}}}
</style>
</head>
<body>
<canvas class="stars" id="stars"></canvas>
<div class="wrap">
  <div class="top"><div class="crest">📚</div><div class="title"><h1>{title}互动挑战</h1><p>{grade}年级{volume} · 快乐读书吧 · {genre}</p></div><span class="badge" id="scoreBadge">积分 0</span></div>
  <div class="steps" id="steps"></div>
  <div class="card" id="scene"></div>
</div>
<script>
const DATA={data_json};
let state={{idx:0,score:0,answered:false}};
const $=s=>document.querySelector(s), scene=$('#scene'), steps=$('#steps'), scoreBadge=$('#scoreBadge');
function shuffle(a){{for(let i=a.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}}return a}}
function renderSteps(){{steps.innerHTML='';DATA.levels.forEach((_,i)=>{{const d=document.createElement('div');d.className='step'+(i<state.idx?' done':'')+(i===state.idx?' cur':'');steps.appendChild(d)}})}}
function renderLevel(){{renderSteps();scoreBadge.textContent='积分 '+state.score;state.answered=false;const lv=DATA.levels[state.idx];const hasImg=lv.image||lv.img;const imgHtml=hasImg?`<div class="stage"><div class="loading">正在打开阅读插画…</div><img alt="场景插画" src="${{lv.image||''}}" onerror="this.src='https://image.pollinations.ai/prompt/'+encodeURIComponent(lv.img||'reading scene')" onload="if(this.previousElementSibling)this.previousElementSibling.remove()"></div>`:'';scene.innerHTML=`<span class="scene-tag">${{lv.tag}}</span>${{imgHtml}}<p class="story">${{lv.story}}</p><div class="qbox"><p class="q">${{lv.q}}</p><p class="hint">${{lv.hint}}</p><div class="opts" id="opts"></div><div class="feedback" id="feedback"></div></div><div class="nav"><button class="btn btn-ghost" id="prevBtn" ${{state.idx===0?'style="display:none"':''}}>← 上一关</button><button class="btn btn-primary" id="nextBtn" disabled>${{state.idx===DATA.levels.length-1?'查看结果 ✦':'下一关 →'}}</button></div>`;const opts=$('#opts');shuffle(lv.opts.slice()).forEach(o=>{{const b=document.createElement('button');b.className='opt';b.textContent=o.t;b.onclick=()=>answer(b,o,lv);opts.appendChild(b)}});$('#nextBtn').onclick=()=>{{state.idx===DATA.levels.length-1?showEnd():(state.idx++,renderLevel())}};const prev=$('#prevBtn');if(prev)prev.onclick=()=>{{state.idx--;renderLevel()}}}}
function answer(btn,opt,lv){{if(state.answered)return;state.answered=true;document.querySelectorAll('.opt').forEach(b=>{{const o=lv.opts.find(x=>x.t===b.textContent);if(o&&o.c)b.classList.add('ok');else if(b===btn)b.classList.add('no')}});const fb=$('#feedback');fb.innerHTML=(opt.c?'🌟 ':'💡 ')+lv.fb;fb.classList.add('show');if(opt.c){{state.score++;scoreBadge.textContent='积分 '+state.score}}$('#nextBtn').disabled=false}}
function showEnd(){{renderSteps();document.querySelectorAll('.step').forEach(s=>s.classList.add('done'));const full=state.score===DATA.levels.length;scene.innerHTML=`<div class="end"><div style="font-size:46px">${{full?'🏅':'📖'}}</div><h2>${{full?'阅读徽章到手':'闯关完成'}}</h2><p class="blurb">你获得 <b style="color:var(--gold)">${{state.score}} / ${{DATA.levels.length}}</b> 分。真正的通关，是能带着文本证据说出自己的理解。</p><div class="create"><h3>最后的创作任务：把阅读变成一张图</h3><p>请写一段图像提示词，包含"谁、在哪里、做什么、画面颜色或心情"。写好后点击生成，看看你的阅读画面会变成什么样。</p><div class="prompt-row"><input id="imagePrompt" value="《{title}》中我最想画的一幕，写清楚谁在哪里做什么，儿童绘本风格，温暖光线"><button class="btn btn-primary" id="imageBtn">生成我的阅读插画</button></div><div class="image-box" id="imageBox"><img id="imageResult" alt="阅读插画"><div class="image-caption" id="imageCaption"></div></div></div><div class="nav"><button class="btn btn-ghost" id="againBtn">再玩一次</button></div></div>`;$('#againBtn').onclick=()=>{{state={{idx:0,score:0,answered:false}};renderLevel()}};$('#imageBtn').onclick=generateImage}}
const AGNES_CFG={{key:'{agnes_key}',base:'{agnes_base}',model:'{agnes_model}'}};
async function agnesImage(prompt){{const finalPrompt=prompt+'，儿童绘本插画，温暖光线，适合小学生阅读分享，无文字';const r=await fetch(AGNES_CFG.base+'/images/generations',{{method:'POST',headers:{{Authorization:'Bearer '+AGNES_CFG.key,'Content-Type':'application/json'}},body:JSON.stringify({{model:AGNES_CFG.model,prompt:finalPrompt,n:1,size:'1024x1024'}})}});if(!r.ok)throw new Error('生图失败 '+r.status);const d=await r.json();const item=(d.data&&d.data[0])||{{}};if(item.url)return item.url;if(item.b64_json)return 'data:image/png;base64,'+item.b64_json;throw new Error('生图返回为空')}}
async function generateImage(){{const input=$('#imagePrompt');const prompt=(input.value||'').trim();if(!prompt){{input.focus();return}}const img=$('#imageResult'),box=$('#imageBox'),caption=$('#imageCaption'),btn=$('#imageBtn');box.style.display='block';caption.textContent='正在生成阅读插画…';btn.disabled=true;try{{img.src=await agnesImage(prompt);caption.textContent='提示词：'+prompt}}catch(e){{caption.textContent='生图失败：'+e.message}}finally{{btn.disabled=false}}}}
(function stars(){{const c=$('#stars'),x=c.getContext('2d');function rs(){{c.width=innerWidth;c.height=innerHeight}}rs();addEventListener('resize',rs);const st=[];for(let i=0;i<80;i++)st.push({{x:Math.random()*c.width,y:Math.random()*c.height,r:Math.random()*1.4+.3,a:Math.random()}});(function draw(){{x.clearRect(0,0,c.width,c.height);st.forEach(s=>{{s.a+=(Math.random()-.5)*.05;if(s.a<.1)s.a=.1;if(s.a>1)s.a=1;x.beginPath();x.arc(s.x,s.y,s.r,0,7);x.fillStyle='rgba(231,198,107,'+(s.a*.65)+')';x.fill()}});requestAnimationFrame(draw)}})()}})();
renderLevel();
</script>
</body>
</html>'''


# ── 主流程 ────────────────────────────────────────────────────────────────

def upgrade_single_book(book_entry, skip_images=False):
    """升级单本推荐书"""
    grade, volume, title, author, genre, brief, text_source = book_entry
    book_id = make_book_id(grade, volume, title)
    html_filename = make_html_filename(book_id)

    author_str = f"（{author}）" if author else ""
    print(f"\n{'='*60}")
    print(f"📚 {grade}年级{volume} · {title}{author_str} [{genre}]")
    print(f"   ID: {book_id}")
    print(f"{'='*60}")

    # 检查是否已经生成过
    html_path = GAMES_DIR / html_filename
    if not skip_images and html_path.exists():
        # 检查是否已有完整的图片
        text = html_path.read_text(encoding="utf-8")
        m = re.search(r"const DATA=(\{.*?\});", text, re.DOTALL)
        if m:
            try:
                data = json.loads(m.group(1))
                levels = data.get("levels", [])
                if len(levels) == 5:
                    all_have_images = all(
                        lv.get("image") and "generated-scenes" in lv.get("image", "")
                        and (ASSETS_DIR / lv["image"].split("/")[-1]).exists()
                        for lv in levels
                    )
                    if all_have_images:
                        print("  ✅ 已有5关个性化题目和本地场景图，跳过重复生成")
                        return True
            except Exception:
                pass

    # 1. 获取书籍文本
    text_content = get_book_text(book_entry)
    print(f"  📄 文本来源: {text_source} ({len(text_content)}字)")

    # 2. 调用 LLM 生成题目
    print(f"  🤖 调用 LLM 生成5关题目...")
    levels = None
    for attempt in range(2):
        try:
            levels = generate_levels_for_book(book_entry, text_content)
            print(f"  ✅ 题目生成成功")
            break
        except Exception as e:
            print(f"  ⚠️  题目生成失败（第{attempt+1}次）: {e}")
            if attempt == 0:
                print("  ⏳ 等待 8s 后重新生成题目...")
                time.sleep(8)
            else:
                traceback.print_exc()
                return False

    # 3. 生成场景图片
    if not skip_images:
        for i, lv in enumerate(levels):
            img_prompt = lv.get("img", "")
            if not img_prompt:
                continue

            img_hash = hashlib.md5(img_prompt.encode()).hexdigest()[:10]
            img_filename = f"rb-{book_id}-{i+1:02d}-{img_hash}.png"
            img_path = ASSETS_DIR / img_filename
            rel_path = f"../../assets/generated-scenes/{img_filename}"

            if img_path.exists():
                print(f"  🖼️  第{i+1}关图片已存在，跳过")
                lv["image"] = rel_path
                continue

            print(f"  🎨 第{i+1}关生图: {img_prompt[:50]}...")
            try:
                generate_image(img_prompt, img_path)
                lv["image"] = rel_path
                print(f"  ✅ 图片已保存: {img_filename}")
                time.sleep(2)
            except Exception as e:
                print(f"  ⚠️  第{i+1}关生图失败: {e}")

    # 4. 构建 DATA 对象
    difficulty_map = {1: "低年级", 2: "低年级", 3: "中年级", 4: "中年级", 5: "高年级", 6: "高年级"}
    data_obj = {
        "item": {
            "kind": "reading",
            "grade": grade,
            "volume": volume,
            "unit": "快乐读书吧",
            "title": title,
            "author": author,
            "genre": genre,
            "brief": brief,
            "difficulty": difficulty_map.get(grade, "低年级"),
        },
        "levels": levels,
    }

    # 5. 生成 HTML 文件
    GAMES_DIR.mkdir(parents=True, exist_ok=True)
    data_json = json.dumps(data_obj, ensure_ascii=False, separators=(",", ":"))

    html_content = HTML_TEMPLATE.format(
        title=title,
        grade=grade,
        volume=volume,
        genre=genre,
        data_json=data_json,
        agnes_key=AGNES_API_KEY,
        agnes_base=AGNES_BASE_URL,
        agnes_model=AGNES_MODEL,
    )

    html_path.write_text(html_content, encoding="utf-8")
    print(f"  📝 HTML 已写入: {html_filename} ({len(html_content)} bytes)")
    print(f"  🎉 升级完成!")
    return True


def update_game_index():
    """更新 game-index.js，替换旧的12个reading条目为新的按书目拆分的条目"""
    text = INDEX_FILE.read_text(encoding="utf-8")

    # 提取现有的 GAME_INDEX
    m = re.search(r"window\.GAME_INDEX\s*=\s*(\[.*?\]);", text, re.DOTALL)
    if not m:
        raise ValueError("无法解析 game-index.js")
    games = json.loads(m.group(1))

    # 移除旧的 reading 条目
    non_reading = [g for g in games if g.get("kind") != "reading"]
    print(f"  移除了 {len(games) - len(non_reading)} 个旧的推荐阅读条目")

    # 构建新的 reading 条目
    difficulty_map = {1: "低年级", 2: "低年级", 3: "中年级", 4: "中年级", 5: "高年级", 6: "高年级"}
    theme_map = {
        "童谣儿歌": "课文博物馆", "儿歌": "课文博物馆",
        "童话故事": "课文博物馆", "童话": "课文博物馆",
        "民间故事": "阅读侦探", "民间": "阅读侦探",
        "寓言": "故事闯关",
        "神话": "阅读侦探",
        "科普": "阅读侦探",
        "儿童故事": "课文博物馆",
        "古典名著": "阅读侦探",
        "成长小说": "故事闯关",
        "世界名著": "课文博物馆",
    }

    new_readings = []
    for i, entry in enumerate(READING_BOOKS):
        grade, volume, title, author, genre, brief, _ = entry
        book_id = make_book_id(grade, volume, title)
        html_filename = make_html_filename(book_id)

        # 验证 HTML 文件是否存在
        if not (GAMES_DIR / html_filename).exists():
            print(f"  ⚠️  跳过 {title}：HTML 文件不存在")
            continue

        new_readings.append({
            "grade": grade,
            "volume": volume,
            "no": i + 1,
            "title": title,
            "author": author,
            "genre": genre,
            "brief": brief,
            "theme": theme_map.get(genre, "课文博物馆"),
            "difficulty": difficulty_map.get(grade, "低年级"),
            "kind": "reading",
            "url": f"games/readings/{html_filename}",
            "refined": True,
            "note": "批量精修：推荐阅读个性化闯关题目 + 场景插画",
        })

    print(f"  新增 {len(new_readings)} 个推荐阅读条目")

    # 合并
    all_games = non_reading + new_readings

    # 写回 game-index.js
    # 保留 SKIPPED_GAME_ITEMS
    skipped_m = re.search(r"window\.SKIPPED_GAME_ITEMS\s*=\s*(\[.*?\]);", text, re.DOTALL)
    skipped_part = ""
    if skipped_m:
        skipped_part = f"\n\nwindow.SKIPPED_GAME_ITEMS = {skipped_m.group(1)};"

    index_json = json.dumps(all_games, ensure_ascii=False, indent=2)
    new_content = f"window.GAME_INDEX = {index_json};{skipped_part}\n"
    INDEX_FILE.write_text(new_content, encoding="utf-8")
    print(f"  ✅ game-index.js 已更新，共 {len(all_games)} 个游戏条目")


def save_progress(completed_ids):
    """保存进度"""
    PROGRESS_FILE.write_text(json.dumps({"completed": list(completed_ids)}, ensure_ascii=False, indent=2), encoding="utf-8")


def load_progress():
    """加载进度"""
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        return set(data.get("completed", []))
    return set()


# ── 入口 ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="批量升级推荐阅读闯关游戏")
    parser.add_argument("--start", type=int, default=0, help="从第几本书开始")
    parser.add_argument("--count", type=int, default=0, help="处理几本（0=全部）")
    parser.add_argument("--skip-images", action="store_true", help="跳过生图")
    parser.add_argument("--resume", action="store_true", help="从上次断点继续")
    parser.add_argument("--dry-run", action="store_true", help="预览书目列表")
    parser.add_argument("--update-index", action="store_true", help="只更新game-index.js")
    args = parser.parse_args()

    books = READING_BOOKS[args.start:]
    if args.count > 0:
        books = books[:args.count]

    print(f"\n📚 推荐阅读批量升级")
    print(f"   共 {len(READING_BOOKS)} 本推荐书目，本次处理 {len(books)} 本")
    print(f"   HTML 输出目录: {GAMES_DIR}")
    print(f"   图片输出目录: {ASSETS_DIR}\n")

    if args.update_index:
        update_game_index()
        return

    if args.dry_run:
        print("=" * 60)
        print("书目预览：")
        print("=" * 60)
        for i, entry in enumerate(books):
            grade, volume, title, author, genre, brief, text_source = entry
            book_id = make_book_id(grade, volume, title)
            author_str = f"（{author}）" if author else ""
            exists = "✅" if (GAMES_DIR / make_html_filename(book_id)).exists() else "❌"
            print(f"  {exists} [{i+1:02d}] {grade}年级{volume} · {title}{author_str} [{genre}] → {book_id}")
        print(f"\n共 {len(books)} 本")
        return

    # 加载进度
    completed = load_progress() if args.resume else set()
    if completed:
        print(f"  📋 已完成 {len(completed)} 本，将跳过")

    # 逐本处理
    success_count = 0
    fail_count = 0

    for i, entry in enumerate(books):
        grade, volume, title, _, _, _, _ = entry
        book_id = make_book_id(grade, volume, title)

        if book_id in completed:
            print(f"\n  ⏭️  跳过已完成: {title} ({book_id})")
            continue

        result = upgrade_single_book(entry, skip_images=args.skip_images)

        if result is True:
            success_count += 1
            completed.add(book_id)
            save_progress(completed)
        elif result is False:
            fail_count += 1
            print(f"  ❌ 生成失败: {title}")

        # 避免API限流
        if i < len(books) - 1:
            time.sleep(4)

    print(f"\n{'='*60}")
    print(f"📊 批量升级完成")
    print(f"   成功: {success_count}")
    print(f"   失败: {fail_count}")
    print(f"   总计: {len(completed)} / {len(READING_BOOKS)}")
    print(f"{'='*60}")

    # 如果全部完成，更新索引
    if len(completed) >= len(READING_BOOKS):
        print("\n🔄 全部书目已完成，正在更新 game-index.js ...")
        update_game_index()


if __name__ == "__main__":
    main()
