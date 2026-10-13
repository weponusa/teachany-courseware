#!/usr/bin/env python3
"""
批量升级阅读闯关游戏：
1. 读取 game-index.js 获取所有游戏条目
2. 匹配每课对应的课文原文
3. 调用 LLM (Paratera DeepSeek-V3.2) 生成 5 关个性化题目
4. 调用 Agnes API 批量生成场景插画
5. 输出精修版 HTML 游戏文件

用法:
  python3 batch_upgrade.py                      # 全量升级
  python3 batch_upgrade.py --start 0 --count 5  # 从第0个开始，升级5个
  python3 batch_upgrade.py --only g3-b-l005      # 只升级指定游戏
  python3 batch_upgrade.py --skip-images         # 跳过生图（只生成题目）
  python3 batch_upgrade.py --resume              # 从上次断点继续
"""

import json, os, sys, re, time, hashlib, argparse, traceback
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# ── 配置 ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
GAMES_DIR = BASE_DIR / "games" / "lessons"
TEXTS_DIR = BASE_DIR / "texts"
ASSETS_DIR = BASE_DIR / "assets" / "generated-scenes"
INDEX_FILE = BASE_DIR / "data" / "game-index.js"
PROGRESS_FILE = BASE_DIR / "scripts" / ".upgrade_progress.json"

# LLM 配置 (Agnes)
LLM_API_KEY = "sk-sizYW5qbTggzJ2liRgzJ9wj7IYGajALpUBtvzOfY86h1BqRE"
LLM_BASE_URL = "https://apihub.agnes-ai.com/v1"
LLM_MODEL = "agnes-2.0-flash"

# Agnes 生图配置
AGNES_API_KEY = "sk-sizYW5qbTggzJ2liRgzJ9wj7IYGajALpUBtvzOfY86h1BqRE"
AGNES_BASE_URL = "https://apihub.agnes-ai.com/v1"
AGNES_MODEL = "agnes-image-2.1-flash"

# 年级映射
GRADE_VOLUME_MAP = {
    (1, "上册"): "一上", (1, "下册"): "一下",
    (2, "上册"): "二上", (2, "下册"): "二下",
    (3, "上册"): "三上", (3, "下册"): "三下",
    (4, "上册"): "四上", (4, "下册"): "四下",
    (5, "上册"): "五上", (5, "下册"): "五下",
    (6, "上册"): "六上", (6, "下册"): "六下",
}

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


def load_game_index():
    """解析 game-index.js 获取游戏列表"""
    text = INDEX_FILE.read_text(encoding="utf-8")
    # 提取 JSON 数组
    m = re.search(r"window\.GAME_INDEX\s*=\s*(\[.*?\]);", text, re.DOTALL)
    if not m:
        raise ValueError("无法解析 game-index.js")
    return json.loads(m.group(1))


def normalize_title(s):
    return re.sub(r'[①②③④⑤⑥⑦⑧⑨⑩◆\s·（）()"“”《》、，。？！：；\-]', '', s or '').lower()


def is_pinyin_title(title):
    compact = normalize_title(title).replace('ü', 'v').replace('ɑ', 'a')
    pinyin_titles = {
        'aoe', 'bpmf', 'dtnl', 'gkh', 'gh', 'jqx', 'zcs', 'zhchshr', 'yw',
        'aieiui', 'aoouiu', 'ieueer', 'ieveer', 'aneninunvn', 'aneninunun', 'angengingong', 'iu'
    }
    return compact in pinyin_titles or (not re.search(r'[\u4e00-\u9fff]', title or '') and bool(compact))


def is_non_reading_game(game):
    """拼音、语文园地、口语交际、识字表等非阅读类内容不参与批量精修。"""
    title = game.get('title', '')
    compact = normalize_title(title)
    if is_pinyin_title(title):
        return True
    if title.startswith(('语文园地', '口语交', '习作')):
        return True
    exact_skip = {
        '天地人', '金木水火土', '口耳目手足', '日月山川', '口耳目', '日月水火',
        '生字表', '识字加油站', '日积月累', '查字典', '一起做游戏', '请你帮个忙',
        '用多大的声音', '我们做朋友', '小兔运南瓜', '读书真快乐'
    }
    return compact in {normalize_title(x) for x in exact_skip}


def find_text_file(game):
    """根据游戏条目找到对应的课文文本文件"""
    grade = game["grade"]
    volume = game["volume"]
    title = game["title"]
    folder_name = GRADE_VOLUME_MAP.get((grade, volume))
    if not folder_name:
        return None

    text_dir = TEXTS_DIR / folder_name
    if not text_dir.exists():
        return None

    # 精确匹配
    exact = text_dir / f"{title}.txt"
    if exact.exists():
        return exact

    # 模糊匹配：去掉特殊字符
    clean_title = normalize_title(title)
    for f in text_dir.iterdir():
        if f.suffix == ".txt":
            clean_name = normalize_title(f.stem)
            if clean_name == clean_title:
                return f

    # 包含匹配：优先完整包含，其次较长关键词相互包含
    for f in text_dir.iterdir():
        if f.suffix != ".txt":
            continue
        clean_name = normalize_title(f.stem)
        if title in f.stem or clean_title in clean_name:
            return f
        if len(clean_name) >= 4 and len(clean_title) >= 4 and (clean_name in clean_title or clean_title in clean_name):
            return f

    return None


def extract_lesson_body(text):
    """从课文文件中提取纯课文内容"""
    lines = text.split("\n")
    body_lines = []
    in_body = False
    for line in lines:
        stripped = line.strip()
        # 跳过元信息头
        if stripped == "课文原文":
            in_body = True
            continue
        if not in_body:
            continue
        # 遇到尾部标记停止
        if stripped in ("课文书影", "相关资料", "+更多教学资料", "无相关信息"):
            break
        # 跳过课后练习提示
        if re.match(r'^(朗读|背诵|默读|分角色|读一读|说一说|读读|小练笔|把课文)', stripped):
            break
        if re.match(r'^◇', stripped):
            break
        body_lines.append(line)

    body = "\n".join(body_lines).strip()
    # 如果没找到"课文原文"标记，用全文（去掉前10行元信息）
    if not body and len(lines) > 10:
        body = "\n".join(lines[10:]).strip()
    return body


def get_game_id_prefix(game):
    """从游戏 URL 中提取 ID 前缀，如 g1-b-l025"""
    url = game.get("url", "")
    m = re.search(r'(g\d+-[ab]-[lr]\d+)', url)
    return m.group(1) if m else None


def get_game_hash(game):
    """从游戏 URL 中提取 hash"""
    url = game.get("url", "")
    m = re.search(r'-([0-9a-f]+)\.html$', url)
    return m.group(1) if m else ""


def html_already_has_images(game):
    """判断现有HTML是否已经包含5关本地场景图，避免重复消耗生图。"""
    html_filename = game.get("url", "").split("/")[-1]
    if not html_filename:
        return False
    html_path = GAMES_DIR / html_filename
    if not html_path.exists():
        return False
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r"const DATA=(\{.*?\});", text, re.DOTALL)
    if not m:
        return False
    try:
        data = json.loads(m.group(1))
    except Exception:
        return False
    levels = data.get("levels", [])
    if len(levels) != 5:
        return False
    for lv in levels:
        image = lv.get("image")
        if not image or "generated-scenes" not in image:
            return False
        filename = image.split("/")[-1]
        if not (ASSETS_DIR / filename).exists():
            return False
    return True


# ── LLM 生成题目 ────────────────────────────────────────────────────────

def generate_levels_with_llm(game, lesson_text):
    """调用 LLM 生成 5 关个性化题目"""
    grade = game["grade"]
    title = game["title"]
    difficulty = game.get("difficulty", "低年级")

    # 根据年级调整提示
    if grade <= 2:
        grade_hint = "1-2年级低年级学生，题目要简单直白，用词浅显，选项简短（每项不超过15字），故事叙述要活泼可爱。"
    elif grade <= 4:
        grade_hint = "3-4年级中年级学生，可以考查理解、推理和写作手法，选项可以稍长（每项不超过25字），故事叙述要有趣味性。"
    else:
        grade_hint = "5-6年级高年级学生，可以考查深层理解、修辞手法、主题思想、作者意图，选项可以有一定深度（每项不超过30字）。"

    prompt = f"""你是一位优秀的小学语文教师，擅长设计互动闯关游戏。

请根据以下课文内容，为《{title}》设计5关闯关题目。

【课文原文】
{lesson_text}

【学生年级】{grade}年级（{difficulty}）
{grade_hint}

【输出要求】
请严格输出以下JSON格式（不要输出任何其他文字），5个关卡对象组成的数组：

```json
[
  {{
    "tag": "第 1 关 · 场景小标题",
    "img": "英文图像提示词，描述该关卡的场景画面，children picture book style, no text",
    "story": "该关卡的场景叙述（50-80字），引用或改编课文中的内容，让学生代入情境",
    "q": "紧扣课文内容的选择题（不超过25字）",
    "hint": "简短提示（不超过20字）",
    "opts": [
      {{"t": "正确选项", "c": true}},
      {{"t": "干扰项1", "c": false}},
      {{"t": "干扰项2", "c": false}},
      {{"t": "干扰项3", "c": false}}
    ],
    "fb": "答题反馈（30-60字），解释为什么正确，联系课文内容"
  }}
]
```

【设计要求】
1. 每关的问题必须紧扣课文原文，考查学生对具体内容的理解（人物、情节、词句、手法、主题等）
2. 5关要覆盖课文的不同段落/方面，形成层层递进
3. story（场景叙述）要自然引用课文中的句子或意象
4. img（图像提示词）必须用英文，描述课文中的具体场景，适合儿童绘本风格
5. 正确答案必须从课文中能找到依据
6. 干扰项要有迷惑性但明显不符合课文
7. 第5关可以设计为整体理解/朗读方法/主题感悟类

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

    # 提取 JSON（可能被 ```json ``` 包裹）
    m = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', content, re.DOTALL)
    if m:
        content = m.group(1)
    else:
        # 尝试直接解析
        content = content.strip()
        if not content.startswith("["):
            # 找第一个 [ 和最后一个 ]
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
        # 下载图片
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
  <div class="top"><div class="crest">阅</div><div class="title"><h1>{title}互动挑战</h1><p>{grade}年级{volume} · {theme}</p></div><span class="badge" id="scoreBadge">积分 0</span></div>
  <div class="steps" id="steps"></div>
  <div class="card" id="scene"></div>
</div>
<script>
const DATA={data_json};
let state={{idx:0,score:0,answered:false}};
const $=s=>document.querySelector(s), scene=$('#scene'), steps=$('#steps'), scoreBadge=$('#scoreBadge');
function hash(s){{let h=0;for(let i=0;i<s.length;i++)h=((h<<5)-h+s.charCodeAt(i))|0;return h}}
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

def upgrade_single_game(game, skip_images=False):
    """升级单个游戏"""
    game_id = get_game_id_prefix(game)
    game_hash = get_game_hash(game)
    title = game["title"]
    grade = game["grade"]
    volume = game["volume"]
    theme = game.get("theme", "课文博物馆")

    print(f"\n{'='*60}")
    print(f"📖 {grade}年级{volume} · {title} ({game_id})")
    print(f"{'='*60}")

    if not skip_images and html_already_has_images(game):
        print("  ✅ 已有5关个性化题目和本地场景图，跳过重复生成")
        return True

    # 1. 查找课文文本；只处理有原文的阅读类课文
    text_file = find_text_file(game)
    if not text_file:
        print(f"  ⚠️  未找到课文文本文件，跳过")
        return None

    raw_text = text_file.read_text(encoding="utf-8")
    lesson_text = extract_lesson_body(raw_text)
    if len(lesson_text) < 5:
        print(f"  ⚠️  课文内容过短（{len(lesson_text)}字），跳过")
        return None

    print(f"  📄 课文文件: {text_file.name} ({len(lesson_text)}字)")

    # 2. 调用 LLM 生成题目
    print(f"  🤖 调用 LLM 生成5关题目...")
    levels = None
    for attempt in range(2):
        try:
            levels = generate_levels_with_llm(game, lesson_text)
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

            img_filename = f"{game_hash}-{i+1:02d}-{hashlib.md5(img_prompt.encode()).hexdigest()[:10]}.png"
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
                time.sleep(2)  # 避免API限流
            except Exception as e:
                print(f"  ⚠️  第{i+1}关生图失败: {e}")
                # 生图失败不影响整体，使用 pollinations 兜底

    # 4. 构建 DATA 对象
    data_obj = {
        "item": {
            "kind": game.get("kind", "lesson"),
            "grade": grade,
            "volume": volume,
            "no": game.get("no", 0),
            "title": title,
            "theme": theme,
            "difficulty": game.get("difficulty", "低年级"),
            "url": game.get("url", ""),
        },
        "levels": levels,
    }

    # 5. 生成 HTML 文件
    html_filename = game.get("url", "").split("/")[-1]
    if not html_filename:
        print(f"  ❌ 无法确定输出文件名")
        return False

    html_path = GAMES_DIR / html_filename
    data_json = json.dumps(data_obj, ensure_ascii=False, separators=(",", ":"))

    html_content = HTML_TEMPLATE.format(
        title=title,
        grade=grade,
        volume=volume,
        theme=theme,
        data_json=data_json,
        agnes_key=AGNES_API_KEY,
        agnes_base=AGNES_BASE_URL,
        agnes_model=AGNES_MODEL,
    )

    html_path.write_text(html_content, encoding="utf-8")
    print(f"  📝 HTML 已写入: {html_filename} ({len(html_content)} bytes)")
    print(f"  🎉 升级完成!")
    return True


def save_progress(completed_ids):
    """保存进度"""
    PROGRESS_FILE.write_text(json.dumps({"completed": completed_ids}, ensure_ascii=False, indent=2), encoding="utf-8")


def load_progress():
    """加载进度"""
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        return set(data.get("completed", []))
    return set()


def main():
    parser = argparse.ArgumentParser(description="批量升级阅读闯关游戏")
    parser.add_argument("--start", type=int, default=0, help="起始索引")
    parser.add_argument("--count", type=int, default=0, help="处理数量（0=全部）")
    parser.add_argument("--only", type=str, default="", help="只处理指定游戏ID（如 g3-b-l005）")
    parser.add_argument("--skip-images", action="store_true", help="跳过生图")
    parser.add_argument("--skip-refined", action="store_true", help="跳过已精修的游戏")
    parser.add_argument("--resume", action="store_true", help="从上次断点继续")
    parser.add_argument("--dry-run", action="store_true", help="只显示将要处理的游戏，不实际执行")
    args = parser.parse_args()

    # 加载游戏列表
    games = load_game_index()
    print(f"📚 共加载 {len(games)} 个游戏条目")

    # 只处理 lesson 类型（不处理 reading 类型）
    lesson_games = [g for g in games if g.get("kind") == "lesson"]
    print(f"📖 其中课文游戏 {len(lesson_games)} 个")

    before_reading_filter = len(lesson_games)
    lesson_games = [g for g in lesson_games if not is_non_reading_game(g)]
    print(f"📘 过滤拼音/非阅读类后剩余 {len(lesson_games)} 个（忽略 {before_reading_filter - len(lesson_games)} 个）")

    # 筛选
    if args.only:
        lesson_games = [g for g in lesson_games if args.only in g.get("url", "")]
        print(f"🎯 指定处理: {args.only}，匹配 {len(lesson_games)} 个")

    if args.skip_refined:
        lesson_games = [g for g in lesson_games if not g.get("refined")]
        print(f"⏭️  跳过已精修，剩余 {len(lesson_games)} 个")

    # 恢复进度
    completed_ids = set()
    if args.resume:
        completed_ids = load_progress()
        before = len(lesson_games)
        lesson_games = [g for g in lesson_games if get_game_id_prefix(g) not in completed_ids]
        print(f"🔄 恢复进度: 已完成 {len(completed_ids)} 个，剩余 {len(lesson_games)} 个")

    # 切片
    if args.start > 0:
        lesson_games = lesson_games[args.start:]
    if args.count > 0:
        lesson_games = lesson_games[:args.count]

    print(f"\n🚀 本次将处理 {len(lesson_games)} 个游戏")
    print(f"   生图: {'跳过' if args.skip_images else '开启'}")

    if args.dry_run:
        print("\n📋 将要处理的游戏列表:")
        for i, g in enumerate(lesson_games):
            text_file = find_text_file(g)
            status = "✅ 有文本" if text_file else "❌ 无文本"
            refined = "🌟精修" if g.get("refined") else ""
            print(f"  {i+1:3d}. {g['grade']}年级{g['volume']} · {g['title']} {status} {refined}")
        return

    # 统计
    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, game in enumerate(lesson_games):
        game_id = get_game_id_prefix(game)
        print(f"\n{'─'*60}")
        print(f"进度: {i+1}/{len(lesson_games)} | 成功: {success_count} | 失败: {fail_count} | 跳过: {skip_count}")

        try:
            ok = upgrade_single_game(game, skip_images=args.skip_images)
            if ok is True:
                success_count += 1
                completed_ids.add(game_id)
                save_progress(list(completed_ids))
            elif ok is None:
                skip_count += 1
                completed_ids.add(game_id)
                save_progress(list(completed_ids))
            else:
                fail_count += 1
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断，保存进度...")
            save_progress(list(completed_ids))
            print(f"已保存进度到 {PROGRESS_FILE}")
            break
        except Exception as e:
            print(f"  ❌ 异常: {e}")
            traceback.print_exc()
            fail_count += 1

        # API 限流保护：LLM 和生图之间增加间隔
        if i < len(lesson_games) - 1:
            print(f"  ⏳ 等待 4s 后继续下一课...")
            time.sleep(4)

    print(f"\n{'='*60}")
    print(f"🏁 批量升级完成!")
    print(f"   成功: {success_count}")
    print(f"   失败: {fail_count}")
    print(f"   跳过: {skip_count}")
    print(f"   总计: {success_count + fail_count + skip_count}")


if __name__ == "__main__":
    main()
