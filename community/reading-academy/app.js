const $ = (selector) => document.querySelector(selector);

const games = window.GAME_INDEX || [];
const els = {
  kindFilter: $('#kindFilter'),
  gradeFilter: $('#gradeFilter'),
  volumeFilter: $('#volumeFilter'),
  gameSelect: $('#gameSelect'),
  playBtn: $('#playBtn'),
  openLink: $('#openLink'),
  readerBtn: $('#readerBtn'),
  practiceBtn: $('#practiceBtn'),
  previewFrame: $('#previewFrame'),
  readerModal: $('#readerModal'),
  closeReader: $('#closeReader'),
  readerTitle: $('#readerTitle'),
  readerKicker: $('#readerKicker'),
  readerBody: $('#readerBody')
};

const GRADE_CN = { 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六' };
let lessonIndex = {};
let bookIndex = [];

async function init() {
  await loadTextIndexes();
  populateGrades();
  bindEvents();
  renderOptions();
}

async function loadTextIndexes() {
  // 优先使用内联 JS 数据（兼容 file:// 协议），回退到 fetch JSON
  if (window.LESSON_INDEX) {
    lessonIndex = window.LESSON_INDEX;
  } else {
    try {
      const r = await fetch('./lesson_index.json');
      lessonIndex = r.ok ? await r.json() : {};
    } catch (_) { lessonIndex = {}; }
  }
  if (window.BOOK_INDEX) {
    bookIndex = window.BOOK_INDEX;
  } else {
    try {
      const r = await fetch('./book_index.json');
      bookIndex = r.ok ? await r.json() : [];
    } catch (_) { bookIndex = []; }
  }
}

function populateGrades() {
  const grades = [...new Set(games.map((item) => item.grade))].sort((a, b) => a - b);
  els.gradeFilter.innerHTML = '<option value="all">全部年级</option>' + grades.map((grade) => `<option value="${grade}">${grade} 年级</option>`).join('');
}

function bindEvents() {
  [els.kindFilter, els.gradeFilter, els.volumeFilter].forEach((el) => el.addEventListener('change', renderOptions));
  els.gameSelect.addEventListener('change', updatePreview);
  els.playBtn.addEventListener('click', () => {
    const game = currentGame();
    if (game) window.open(`./${game.url}`, '_blank', 'noopener');
  });
  els.readerBtn.addEventListener('click', openCurrentReader);
  els.closeReader.addEventListener('click', closeReader);
  els.readerModal.addEventListener('click', (event) => { if (event.target === els.readerModal) closeReader(); });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeReader(); });
}

function filteredGames() {
  const kind = els.kindFilter.value;
  const grade = els.gradeFilter.value;
  const volume = els.volumeFilter.value;
  return games.filter((item) => {
    if (kind !== 'all' && item.kind !== kind) return false;
    if (grade !== 'all' && String(item.grade) !== grade) return false;
    if (volume !== 'all' && item.volume !== volume) return false;
    return true;
  }).sort((a, b) => Number(Boolean(b.refined)) - Number(Boolean(a.refined)) || a.grade - b.grade || String(a.volume).localeCompare(String(b.volume)) || Number(a.no || 0) - Number(b.no || 0));
}

function renderOptions() {
  const list = filteredGames();
  els.gameSelect.innerHTML = list.map((item) => `<option value="${escapeAttr(item.url)}">${item.refined ? '★ ' : ''}${item.grade}年级${item.volume} · ${escapeHtml(item.title)}</option>`).join('');
  updatePreview();
}

function currentGame() {
  return games.find((item) => item.url === els.gameSelect.value);
}

function updatePreview() {
  const game = currentGame();
  if (!game) {
    els.previewFrame.removeAttribute('src');
    els.openLink.removeAttribute('href');
    els.practiceBtn.removeAttribute('href');
    return;
  }
  els.previewFrame.src = `./${game.url}`;
  els.openLink.href = `./${game.url}`;
  updatePracticeLink(game);
}

function updatePracticeLink(game) {
  const params = new URLSearchParams({
    grade: GRADE_CN[game.grade] || String(game.grade),
    volume: game.volume.includes('上') ? '上' : '下',
    lesson: game.title
  });
  els.practiceBtn.href = `../明湾生字工具/语文生字练习.html?${params.toString()}`;
}

async function openCurrentReader() {
  const game = currentGame();
  if (!game) return;
  els.readerKicker.textContent = `${game.grade}年级${game.volume} · ${game.kind === 'reading' ? '推荐阅读' : '课文'}`;
  els.readerTitle.textContent = game.title;
  els.readerBody.innerHTML = '<p class="reader-loading">正在打开本地原文...</p>';
  openReader();

  // 获取当前课的生字列表
  const charList = getCharListForGame(game);

  // 优先从内联数据中查找（兼容 file:// 协议）
  const inlineText = findInlineText(game);
  if (inlineText) {
    els.readerBody.innerHTML = renderEnhancedText(extractLessonBody(inlineText), game, charList);
    return;
  }

  // 回退到 fetch 加载 txt 文件
  const candidates = buildTextCandidates(game);
  for (const path of candidates) {
    try {
      const res = await fetch(path);
      if (!res.ok) continue;
      const text = await res.text();
      els.readerBody.innerHTML = renderEnhancedText(extractLessonBody(text), game, charList);
      return;
    } catch (error) {
      // try next path
    }
  }
  els.readerBody.innerHTML = `<p class="reader-loading">暂时没有找到《${escapeHtml(game.title)}》的本地原文。可以继续闯关，或补充对应 txt 文件。</p>`;
}

function findInlineText(game) {
  if (!window.TEXT_DATA) return null;
  const td = window.TEXT_DATA;

  if (game.kind === 'lesson') {
    const key = `${GRADE_CN[game.grade] || game.grade}${game.volume.includes('上') ? '上' : '下'}`;
    // 方式1：通过 lessonIndex 匹配
    const names = lessonIndex[key] || [];
    const matched = findMatchingName(names, game.title);
    if (matched && td[`${key}/${matched}`]) return td[`${key}/${matched}`];
    // 方式2：直接用游戏标题作为 key
    if (td[`${key}/${game.title}`]) return td[`${key}/${game.title}`];
    // 方式3：遍历 TEXT_DATA 中该册次的所有 key 进行模糊匹配
    const prefix = `${key}/`;
    const target = normalizeTitle(game.title);
    for (const k of Object.keys(td)) {
      if (!k.startsWith(prefix)) continue;
      const name = k.slice(prefix.length);
      if (normalizeTitle(name) === target || normalizeTitle(name).includes(target) || target.includes(normalizeTitle(name))) {
        return td[k];
      }
    }
    // 方式4：跨册次回退
    const altVol = game.volume.includes('上') ? '下' : '上';
    const altKey = `${GRADE_CN[game.grade] || game.grade}${altVol}`;
    const altPrefix = `${altKey}/`;
    for (const k of Object.keys(td)) {
      if (!k.startsWith(altPrefix)) continue;
      const name = k.slice(altPrefix.length);
      if (normalizeTitle(name) === target || normalizeTitle(name).includes(target) || target.includes(normalizeTitle(name))) {
        return td[k];
      }
    }
  }

  if (game.kind === 'reading') {
    // 方式1：通过 bookIndex 匹配
    const matched = findMatchingName(bookIndex, game.title);
    const readingPrefix = '快乐读书吧/';
    if (matched && td[`${readingPrefix}${matched}`]) return td[`${readingPrefix}${matched}`];
    if (td[`${readingPrefix}${game.title}`]) return td[`${readingPrefix}${game.title}`];
    // 方式2：遍历 TEXT_DATA 中推荐阅读的所有 key 进行模糊匹配
    const target = normalizeTitle(game.title);
    for (const k of Object.keys(td)) {
      if (!k.startsWith(readingPrefix)) continue;
      const name = k.slice(readingPrefix.length);
      if (normalizeTitle(name) === target || normalizeTitle(name).includes(target) || target.includes(normalizeTitle(name))) {
        return td[k];
      }
    }
  }

  return null;
}

function buildTextCandidates(game) {
  if (game.kind === 'reading') {
    const matched = findMatchingName(bookIndex, game.title);
    return matched ? [`./texts/快乐读书吧/${encodeURIComponent(matched)}.txt`] : [`./texts/快乐读书吧/${encodeURIComponent(game.title)}.txt`];
  }

  const key = `${GRADE_CN[game.grade] || game.grade}${game.volume.includes('上') ? '上' : '下'}`;
  const names = lessonIndex[key] || [];
  const matched = findMatchingName(names, game.title);
  const paths = [];
  if (matched) paths.push(`./texts/${encodeURIComponent(key)}/${encodeURIComponent(matched)}.txt`);
  paths.push(`./texts/${encodeURIComponent(key)}/${encodeURIComponent(game.title)}.txt`);

  // 跨年级回退搜索（某些课文在相邻册次目录）
  const vol = game.volume.includes('上') ? '上' : '下';
  const altVol = vol === '上' ? '下' : '上';
  const altKey = `${GRADE_CN[game.grade] || game.grade}${altVol}`;
  const altNames = lessonIndex[altKey] || [];
  const altMatched = findMatchingName(altNames, game.title);
  if (altMatched) paths.push(`./texts/${encodeURIComponent(altKey)}/${encodeURIComponent(altMatched)}.txt`);

  return [...new Set(paths)];
}

function findMatchingName(names, title) {
  const target = normalizeTitle(title);
  return names.find((name) => normalizeTitle(name) === target) || names.find((name) => normalizeTitle(name).includes(target) || target.includes(normalizeTitle(name)));
}

function normalizeTitle(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[\s·・.。．,，、:：;；!！?？"""'''\u201c\u201d\u2018\u2019《》()（）\[\]【】_\-\u00b7\u2022\u2026\u2014\u2013]/g, '')
    .replace(/ü/g, 'v')
    .replace(/两/g, '二')
    .replace(/词/g, '');
}

function extractLessonBody(text) {
  const lines = text.split(/\r?\n/);
  const start = lines.findIndex((line) => line.trim() === '课文原文');
  const slice = start >= 0 ? lines.slice(start + 1) : lines;
  const stop = slice.findIndex((line) => /课文书影|相关资料|教学反思|教案|说课稿|课件|\+更多/.test(line));
  return (stop >= 0 ? slice.slice(0, stop) : slice).join('\n');
}

function cleanLines(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !isNoiseLine(line));
}

function isNoiseLine(line) {
  return line === '汉查查' || line === '»' ||
    /^\d{4}-\d{2}-\d{2}/.test(line) ||
    ['语文', '课文', '课文原文', '相关资料', '课文书影'].includes(line) ||
    /年级[上下]册语文$/.test(line) ||
    /课堂笔记|教学设计|同步练习|生字组词|知识点|教学反思|教案|说课稿|课件/.test(line) ||
    /^\+更多/.test(line);
}

/* ─── 生字索引查找 ─── */
function getCharListForGame(game) {
  const ci = window.CHAR_INDEX;
  if (!ci || game.kind !== 'lesson') return [];
  const key = `${GRADE_CN[game.grade] || game.grade}${game.volume.includes('上') ? '上' : '下'}/${game.title}`;
  if (ci[key]) return ci[key];
  // 模糊匹配
  const target = normalizeTitle(game.title);
  for (const k of Object.keys(ci)) {
    const name = k.split('/').pop();
    if (normalizeTitle(name) === target) return ci[k];
  }
  return [];
}

/* ─── 智能排版引擎 ─── */
function renderEnhancedText(text, game, charList) {
  const lines = cleanLines(text);
  if (!lines.length) return '<p class="reader-loading">暂无内容。</p>';

  // 构建生字 map：{ 字: 拼音 }
  const charMap = {};
  (charList || []).forEach((ch) => { charMap[ch.c] = ch.p; });

  const isPoem = detectPoem(lines, game);
  const html = [];
  let firstLine = true;
  let inQuoteBlock = false;

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const line = raw.trim();

    // ── 跳过课后题干、读写提示 ──
    if (/^(读[一下]读|说[一下]说|朗读课文|默读课文|背诵|试着|◇|☆|●|读下面|抄写|选做)/.test(line)) break;

    // ── 标题行 ──
    if (firstLine) {
      firstLine = false;
      // 第一行通常是课文标题，可能带序号前缀 ①②③ 或数字
      const titleText = line.replace(/^[①②③④⑤⑥⑦⑧⑨⑩\d]+[.、．\s]*/, '');
      html.push(`<h3 class="rt-title">${escapeHtml(titleText)}</h3>`);
      continue;
    }

    // ── 作者行（紧跟标题后，短且含方括号或朝代或常见格式）──
    if (html.length === 1 && isAuthorLine(line)) {
      html.push(`<p class="rt-author">${escapeHtml(line)}</p>`);
      continue;
    }

    // ── 分节标记 ──
    if (/^[一二三四五六七八九十]+$/.test(line) || /^第[一二三四五六七八九十\d]+[章节段幕]/.test(line)) {
      html.push(`<h4 class="rt-section">${escapeHtml(line)}</h4>`);
      continue;
    }

    // ── 引文/名言（整行被引号包裹，或以"谚语""俗话说"开头）──
    if (/^[""\u201c].*[""\u201d]$/.test(line) && line.length < 60) {
      html.push(`<blockquote class="rt-quote">${annotateChars(escapeHtml(line), charMap)}</blockquote>`);
      continue;
    }

    // ── 诗歌模式 ──
    if (isPoem) {
      html.push(`<p class="rt-verse">${annotateChars(escapeHtml(line), charMap)}</p>`);
      continue;
    }

    // ── 普通段落 ──
    const annotated = annotateChars(escapeHtml(line), charMap);
    // 对话行（以引号开头）
    if (/^["""\u201c]/.test(line)) {
      html.push(`<p class="rt-dialogue">${annotated}</p>`);
    } else {
      html.push(`<p>${annotated}</p>`);
    }
  }

  // 生字表卡片
  if (charList && charList.length > 0) {
    html.push(renderCharCard(charList));
  }

  return html.join('\n');
}

function detectPoem(lines, game) {
  // 古诗/儿歌/歌谣检测
  const title = (game && game.title) || '';
  if (/古诗|诗[二三四]首|绝句|律诗|七律|五律|词[二三]首|浪淘沙|渔歌子|忆江南|清平乐|卜算子/.test(title)) return true;
  // 短行密集（80%的行 < 20字，且总行数 < 40）
  if (lines.length > 2 && lines.length < 40) {
    const shortCount = lines.filter((l) => l.trim().length > 0 && l.trim().length < 22).length;
    const nonEmpty = lines.filter((l) => l.trim().length > 0).length;
    if (nonEmpty > 0 && shortCount / nonEmpty > 0.75) return true;
  }
  return false;
}

function isAuthorLine(line) {
  if (line.length > 30) return false;
  // [唐] 李白 / 〔宋〕辛弃疾 / 作者：xxx / ——鲁迅
  return /^[\[〔【（(].*[\]〕】）)]/.test(line) ||
    /^(作者|文|图|——|—)/.test(line) ||
    /^\[.{1,4}\]\s*.+$/.test(line);
}

function annotateChars(htmlLine, charMap) {
  if (!charMap || Object.keys(charMap).length === 0) return htmlLine;
  // 在已转义的 HTML 中查找生字并加 ruby 注音
  let result = '';
  for (let i = 0; i < htmlLine.length; i++) {
    const ch = htmlLine[i];
    // 跳过 HTML 实体（&amp; &lt; 等）
    if (ch === '&') {
      const semiIdx = htmlLine.indexOf(';', i);
      if (semiIdx > i && semiIdx - i < 8) {
        result += htmlLine.slice(i, semiIdx + 1);
        i = semiIdx;
        continue;
      }
    }
    if (charMap[ch]) {
      result += `<ruby class="rt-char">${ch}<rp>(</rp><rt>${charMap[ch]}</rt><rp>)</rp></ruby>`;
    } else {
      result += ch;
    }
  }
  return result;
}

function renderCharCard(charList) {
  const items = charList.map((ch) =>
    `<span class="cc-item"><ruby>${escapeHtml(ch.c)}<rp>(</rp><rt>${escapeHtml(ch.p)}</rt><rp>)</rp></ruby></span>`
  ).join('');
  return `<div class="char-card">
    <div class="cc-head"><span class="cc-icon">✏️</span> 本课生字 <span class="cc-count">${charList.length}个</span></div>
    <div class="cc-grid">${items}</div>
  </div>`;
}

function renderTextAsParagraphs(text) {
  const lines = cleanLines(text);
  if (!lines.length) return '<p class="reader-loading">暂无内容。</p>';
  return lines.map((line) => `<p>${escapeHtml(line)}</p>`).join('');
}

function openReader() {
  els.readerModal.classList.add('show');
  els.readerModal.setAttribute('aria-hidden', 'false');
}

function closeReader() {
  els.readerModal.classList.remove('show');
  els.readerModal.setAttribute('aria-hidden', 'true');
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
}

function escapeAttr(value) {
  return escapeHtml(value).replace(/`/g, '&#96;');
}

/* ═══════════════════════════════════════════════════════
   ✨ 自制游戏模块 — 自选书目 → AI 生成闯关游戏
   ═══════════════════════════════════════════════════════ */

const AGNES_LLM = {
  key: 'sk-sizYW5qbTggzJ2liRgzJ9wj7IYGajALpUBtvzOfY86h1BqRE',
  base: 'https://apihub.agnes-ai.com/v1',
  model: 'agnes-2.0-flash',
  imageModel: 'agnes-image-2.1-flash',
};

/* ─── 预设书目库 ─── */
const PRESET_BOOKS = {
  hp: [
    { title: '哈利·波特与魔法石', author: 'J.K.罗琳', grade: 4, brief: '11岁的哈利·波特发现自己是巫师，进入霍格沃茨魔法学校，结识罗恩和赫敏，勇闯密室保护魔法石。' },
    { title: '哈利·波特与密室', author: 'J.K.罗琳', grade: 4, brief: '霍格沃茨出现恐怖袭击，学生接连被石化。哈利发现密室的秘密，勇斗蛇怪和伏地魔的记忆。' },
    { title: '哈利·波特与阿兹卡班的囚徒', author: 'J.K.罗琳', grade: 5, brief: '逃犯小天狼星布莱克越狱，传说他要找哈利。哈利学会了守护神咒，发现了父亲好友的真相。' },
    { title: '哈利·波特与火焰杯', author: 'J.K.罗琳', grade: 5, brief: '三强争霸赛在霍格沃茨举行，哈利意外成为第四位勇士。决赛中他目睹伏地魔复活。' },
    { title: '哈利·波特与凤凰社', author: 'J.K.罗琳', grade: 5, brief: '魔法部否认伏地魔归来，哈利在邓布利多军中教同学们战斗魔法，最终在神秘事务司展开激战。' },
    { title: '哈利·波特与混血王子', author: 'J.K.罗琳', grade: 6, brief: '哈利获得一本神秘的魔药课本，发现"混血王子"的身份。邓布利多与哈利追查伏地魔的魂器。' },
    { title: '哈利·波特与死亡圣器', author: 'J.K.罗琳', grade: 6, brief: '哈利、罗恩、赫敏离开学校，踏上寻找和摧毁魂器的旅程。最终在霍格沃茨大战中击败伏地魔。' },
  ],
  verne: [
    { title: '海底两万里', author: '儒勒·凡尔纳', grade: 4, brief: '阿罗纳克斯教授和仆人康塞尔、鱼叉手尼德·兰登上神秘的鹦鹉螺号潜水艇，与尼摩船长环游海底世界。' },
    { title: '八十天环游地球', author: '儒勒·凡尔纳', grade: 4, brief: '英国绅士福格与仆人路路通打赌80天环游地球。他们乘火车、轮船、大象，经历无数冒险，最终分秒不差赢得赌约。' },
    { title: '地心游记', author: '儒勒·凡尔纳', grade: 5, brief: '利登布洛克教授带着侄子阿克塞尔和向导汉斯，从冰岛火山口进入地球内部，发现史前生物和地下海洋。' },
    { title: '神秘岛', author: '儒勒·凡尔纳', grade: 5, brief: '五个人乘气球逃离战俘营，流落到太平洋荒岛。他们凭借智慧和勇气建设家园，并发现了尼摩船长的秘密。' },
    { title: '格兰特船长的儿女', author: '儒勒·凡尔纳', grade: 5, brief: '格里那凡爵士在鲨鱼腹中发现漂流瓶，带领船队沿南纬37度线环球搜索失踪的格兰特船长。' },
    { title: '从地球到月球', author: '儒勒·凡尔纳', grade: 5, brief: '美国南北战争后，大炮俱乐部主席巴比凯恩提议制造巨型大炮将飞行器射向月球，三人登上炮弹开始月球之旅。' },
    { title: '环游月球', author: '儒勒·凡尔纳', grade: 5, brief: '三位旅行者在炮弹飞行器中绕月飞行，近距离观察月球表面，经历失重和陨石撞击，最终成功返回地球。' },
    { title: '十五岁的船长', author: '儒勒·凡尔纳', grade: 5, brief: '15岁的迪克·桑德在船长遇难后接管指挥权，带领船员们穿越非洲大陆，与奴隶贩子斗智斗勇。' },
    { title: '气球上的五星期', author: '儒勒·凡尔纳', grade: 4, brief: '弗格森博士乘坐热气球从东非桑给巴尔岛出发，横穿非洲大陆上空，历经五个星期的惊险飞行。' },
    { title: '机器岛', author: '儒勒·凡尔纳', grade: 6, brief: '一座由钢铁建造的巨型人工浮岛在太平洋上航行，岛上的亿万富翁们过着奢华生活，却因内部矛盾走向毁灭。' },
  ],
};

let selectedBooks = [];

function initCustomGame() {
  const btn = $('#customGameBtn');
  const modal = $('#customModal');
  const closeBtn = $('#closeCustom');
  if (!btn || !modal) return;

  // 渲染预设书目
  renderPresetList('hpList', PRESET_BOOKS.hp);
  renderPresetList('verneList', PRESET_BOOKS.verne);

  // 事件绑定
  btn.addEventListener('click', () => { modal.classList.add('show'); modal.setAttribute('aria-hidden', 'false'); });
  closeBtn.addEventListener('click', closeCustomModal);
  modal.addEventListener('click', (e) => { if (e.target === modal) closeCustomModal(); });

  // 全选按钮
  document.querySelectorAll('.select-all-btn').forEach((b) => {
    b.addEventListener('click', () => {
      const series = b.dataset.series;
      const books = PRESET_BOOKS[series];
      const allSelected = books.every((bk) => selectedBooks.some((s) => s.title === bk.title));
      if (allSelected) {
        books.forEach((bk) => { selectedBooks = selectedBooks.filter((s) => s.title !== bk.title); });
      } else {
        books.forEach((bk) => { if (!selectedBooks.some((s) => s.title === bk.title)) selectedBooks.push({ ...bk }); });
      }
      refreshAllChips();
      renderSelectedList();
    });
  });

  // 添加自定义书籍
  $('#addCustomBook').addEventListener('click', addCustomBook);

  // 生成按钮
  $('#generateBtn').addEventListener('click', generateCustomGames);
}

function renderPresetList(containerId, books) {
  const container = $(`#${containerId}`);
  container.innerHTML = books.map((bk) => {
    const active = selectedBooks.some((s) => s.title === bk.title) ? ' active' : '';
    return `<span class="preset-chip${active}" data-title="${escapeAttr(bk.title)}">
      <span class="chip-check">${active ? '✓' : ''}</span>${escapeHtml(bk.title)}
    </span>`;
  }).join('');

  container.querySelectorAll('.preset-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      const title = chip.dataset.title;
      const book = books.find((b) => b.title === title);
      if (!book) return;
      const idx = selectedBooks.findIndex((s) => s.title === title);
      if (idx >= 0) {
        selectedBooks.splice(idx, 1);
        chip.classList.remove('active');
        chip.querySelector('.chip-check').textContent = '';
      } else {
        selectedBooks.push({ ...book });
        chip.classList.add('active');
        chip.querySelector('.chip-check').textContent = '✓';
      }
      renderSelectedList();
    });
  });
}

function refreshAllChips() {
  document.querySelectorAll('.preset-chip').forEach((chip) => {
    const title = chip.dataset.title;
    const isSelected = selectedBooks.some((s) => s.title === title);
    chip.classList.toggle('active', isSelected);
    chip.querySelector('.chip-check').textContent = isSelected ? '✓' : '';
  });
}

function addCustomBook() {
  const title = ($('#customTitle').value || '').trim();
  if (!title) { $('#customTitle').focus(); return; }
  if (selectedBooks.some((s) => s.title === title)) { alert('这本书已经在列表中了'); return; }
  const author = ($('#customAuthor').value || '').trim();
  const grade = parseInt($('#customGrade').value) || 4;
  const brief = ($('#customBrief').value || '').trim();
  selectedBooks.push({ title, author, grade, brief, custom: true });
  // 清空输入
  $('#customTitle').value = '';
  $('#customAuthor').value = '';
  $('#customBrief').value = '';
  renderSelectedList();
}

function renderSelectedList() {
  const list = $('#selectedList');
  const count = $('#selectedCount');
  const genBtn = $('#generateBtn');
  count.textContent = selectedBooks.length;
  genBtn.disabled = selectedBooks.length === 0;
  list.innerHTML = selectedBooks.map((bk, i) => {
    const icon = bk.custom ? '✏️' : '📖';
    return `<span class="selected-tag">${icon} ${escapeHtml(bk.title)}<span class="remove-tag" data-idx="${i}">×</span></span>`;
  }).join('');
  list.querySelectorAll('.remove-tag').forEach((btn) => {
    btn.addEventListener('click', () => {
      selectedBooks.splice(parseInt(btn.dataset.idx), 1);
      refreshAllChips();
      renderSelectedList();
    });
  });
}

function closeCustomModal() {
  const modal = $('#customModal');
  modal.classList.remove('show');
  modal.setAttribute('aria-hidden', 'true');
}

/* ─── AI 生成游戏 ─── */
async function generateCustomGames() {
  if (selectedBooks.length === 0) return;
  const genBtn = $('#generateBtn');
  const status = $('#generateStatus');
  genBtn.disabled = true;

  const total = selectedBooks.length;
  let done = 0;

  // 逐本生成
  for (const book of selectedBooks) {
    done++;
    status.innerHTML = `⏳ 正在为《${escapeHtml(book.title)}》生成闯关题目... (${done}/${total})
      <span class="progress-bar"><span class="progress-fill" style="width:${Math.round((done - 0.5) / total * 100)}%"></span></span>`;

    try {
      const levels = await generateLevelsForBook(book);
      const gameHtml = buildGameHtml(book, levels);
      // 写入 blob URL 并在 iframe 中预览
      const blob = new Blob([gameHtml], { type: 'text/html;charset=utf-8' });
      const blobUrl = URL.createObjectURL(blob);

      // 注册到游戏列表以供切换
      const gameEntry = {
        kind: 'custom',
        grade: book.grade,
        volume: '自制',
        title: book.title,
        url: blobUrl,
        blobUrl: true,
        refined: false,
      };
      games.push(gameEntry);

      status.innerHTML = `✅ 《${escapeHtml(book.title)}》生成完成！(${done}/${total})
        <span class="progress-bar"><span class="progress-fill" style="width:${Math.round(done / total * 100)}%"></span></span>`;
    } catch (err) {
      console.error(`生成 ${book.title} 失败:`, err);
      status.innerHTML = `❌ 《${escapeHtml(book.title)}》生成失败: ${escapeHtml(err.message)} (${done}/${total})`;
    }
  }

  // 全部完成
  status.innerHTML = `🎉 全部完成！已生成 ${total} 个游戏，请在下拉列表中选择"自制"类型查看`;
  genBtn.disabled = false;

  // 刷新筛选器（添加 custom 类型选项）
  if (!els.kindFilter.querySelector('option[value="custom"]')) {
    els.kindFilter.insertAdjacentHTML('beforeend', '<option value="custom">✨ 自制游戏</option>');
  }
  // 自动切换到自制游戏
  els.kindFilter.value = 'custom';
  renderOptions();

  // 自制游戏的预览要特殊处理 blob URL
  closeCustomModal();
  selectedBooks = [];
  renderSelectedList();
  refreshAllChips();
}

async function generateLevelsForBook(book) {
  const difficultyHint = book.grade <= 2 ? '适合1-2年级学生，题目简单有趣，选项字数控制在6字以内' :
    book.grade <= 4 ? '适合3-4年级学生，题目考察阅读理解和推理能力' :
    '适合5-6年级学生，题目可以考察深层理解、人物分析、主题思考';

  const prompt = `你是小学语文阅读教学专家。请根据下面的书籍信息，设计5道闯关阅读理解选择题。

书名：${book.title}
作者：${book.author || '未知'}
${book.brief ? '简介：' + book.brief : ''}
难度要求：${difficultyHint}

要求：
1. 每关围绕书中一个精彩场景或关键情节
2. 故事叙述要生动有画面感，50-80字
3. 每题4个选项，正好1个正确
4. 反馈解说要有知识性和趣味性，30-60字
5. img字段写英文图像提示词，描述该场景的儿童绘本插画

严格输出JSON数组，不要任何其他文字：
[{"tag":"第 1 关 · 场景标题","img":"英文图像提示词","story":"场景叙述","q":"选择题","hint":"提示","opts":[{"t":"选项","c":true},{"t":"选项","c":false},{"t":"选项","c":false},{"t":"选项","c":false}],"fb":"反馈"}]`;

  const resp = await fetch(`${AGNES_LLM.base}/chat/completions`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${AGNES_LLM.key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: AGNES_LLM.model,
      messages: [
        { role: 'system', content: '你是小学语文教学专家，只输出JSON数组，不输出任何其他内容。' },
        { role: 'user', content: prompt }
      ],
      temperature: 0.7,
      max_tokens: 4000,
    }),
  });

  if (!resp.ok) throw new Error(`AI接口错误 ${resp.status}`);
  const data = await resp.json();
  const text = (data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content) || '';

  // 解析 JSON
  let levels;
  const jsonMatch = text.match(/```json\s*([\s\S]*?)```/) || text.match(/(\[[\s\S]*\])/);
  if (jsonMatch) {
    levels = JSON.parse(jsonMatch[1]);
  } else {
    throw new Error('AI返回格式异常');
  }

  // 校验
  if (!Array.isArray(levels) || levels.length < 3) throw new Error('生成关卡数不足');
  levels = levels.slice(0, 5); // 最多5关
  for (const lv of levels) {
    if (!lv.tag || !lv.q || !Array.isArray(lv.opts) || lv.opts.length < 3) {
      throw new Error('关卡数据不完整');
    }
  }
  return levels;
}

function buildGameHtml(book, levels) {
  const dataObj = {
    item: {
      kind: 'custom',
      grade: book.grade,
      volume: '自制',
      title: book.title,
      author: book.author || '',
      difficulty: book.grade <= 2 ? '低年级' : book.grade <= 4 ? '中年级' : '高年级',
    },
    levels: levels,
  };
  const dataJson = JSON.stringify(dataObj);
  const safeTitle = escapeHtml(book.title);
  const agnesKey = AGNES_LLM.key;
  const agnesBase = AGNES_LLM.base;
  const agnesModel = AGNES_LLM.imageModel;

  return `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${safeTitle}互动挑战</title>
<style>
:root{--bg:#0f1022;--panel:#1b1d3d;--panel2:#242752;--gold:#e7c66b;--ink:#f8f0d8;--muted:#c4bddb;--line:rgba(231,198,107,.24);--ok:#62d99a;--no:#e98175}
*{box-sizing:border-box}html,body{margin:0}body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:radial-gradient(1000px 540px at 50% -10%,#34466f 0%,transparent 62%),radial-gradient(900px 520px at 100% 100%,#253d34 0%,transparent 55%),var(--bg);color:var(--ink);min-height:100vh}.stars{position:fixed;inset:0;pointer-events:none;opacity:.42}.wrap{position:relative;z-index:1;max-width:840px;margin:0 auto;padding:18px 16px 58px}.top{display:flex;align-items:center;gap:12px;margin-bottom:14px}.crest{width:48px;height:48px;border-radius:14px;overflow:hidden;border:1px solid var(--line);display:grid;place-items:center;padding:0;background:#111}.crest img{width:100%;height:100%;object-fit:cover;display:block}.title h1{font-size:19px;margin:0}.title p{margin:3px 0 0;font-size:12px;color:var(--muted)}.badge{margin-left:auto;font-size:12px;color:var(--gold);background:rgba(231,198,107,.1);border:1px solid var(--line);border-radius:999px;padding:6px 12px}.steps{display:flex;gap:6px;margin:0 0 16px}.step{flex:1;height:6px;border-radius:999px;background:rgba(255,255,255,.08)}.step.done{background:var(--gold)}.step.cur{background:linear-gradient(90deg,var(--gold),rgba(231,198,107,.2))}.card{background:linear-gradient(180deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:0 22px 56px rgba(0,0,0,.34)}.scene-tag{display:inline-block;font-size:12px;color:var(--gold);background:rgba(231,198,107,.1);border:1px solid var(--line);border-radius:999px;padding:5px 12px;margin-bottom:14px}.stage{position:relative;width:100%;aspect-ratio:16/10;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#111831;margin-bottom:15px}.stage img{width:100%;height:100%;object-fit:cover;display:block}.stage .loading{position:absolute;inset:0;display:grid;place-items:center;color:var(--muted);background:linear-gradient(135deg,rgba(255,255,255,.04),rgba(0,0,0,.18));text-align:center;padding:20px}.story{font-size:15px;line-height:1.9;margin:0 0 12px}.story em{font-style:normal;color:var(--gold)}.qbox{margin-top:16px;padding-top:16px;border-top:1px dashed var(--line)}.q{font-size:18px;font-weight:800;line-height:1.65;margin:0 0 4px}.hint{font-size:12px;color:var(--muted);margin:0 0 12px}.opts{display:grid;gap:10px}.opt{text-align:left;font-size:14px;line-height:1.55;padding:14px 15px;border-radius:14px;border:1px solid var(--line);background:rgba(255,255,255,.04);color:var(--ink);cursor:pointer;font-family:inherit}.opt:hover{border-color:var(--gold);background:rgba(231,198,107,.08)}.opt.ok{border-color:var(--ok);background:rgba(98,217,154,.14);color:#c8f7df}.opt.no{border-color:var(--no);background:rgba(233,129,117,.14);color:#ffd0ca}.feedback{display:none;margin-top:14px;padding:14px 15px;border-radius:14px;font-size:13px;line-height:1.8;border:1px solid var(--line);background:rgba(231,198,107,.07)}.feedback.show{display:block}.nav{display:flex;gap:10px;margin-top:16px}button{font-family:inherit}.btn{flex:1;border:0;border-radius:14px;padding:13px;font-size:14px;font-weight:800;cursor:pointer}.btn-primary{background:linear-gradient(180deg,var(--gold),#bd9343);color:#241b08}.btn-primary:disabled{opacity:.45;cursor:default}.btn-ghost{background:rgba(255,255,255,.06);color:var(--muted);border:1px solid var(--line)}.end{text-align:center;padding:10px 0}.end h2{color:var(--gold);font-size:26px;margin:8px 0}.blurb{font-size:15px;line-height:1.9;color:var(--ink)}.create{margin-top:18px;text-align:left;border:1px solid var(--line);border-radius:18px;padding:16px;background:rgba(255,255,255,.05)}.create h3{margin:0 0 8px;color:var(--gold)}.create p{margin:0 0 12px;color:var(--muted);line-height:1.75;font-size:13px}.prompt-row{display:flex;gap:8px}.prompt-row input{flex:1;border:1px solid var(--line);border-radius:12px;background:rgba(0,0,0,.22);color:var(--ink);padding:12px;font:inherit}.image-box{display:none;margin-top:14px;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#111}.image-box img{display:block;width:100%;height:auto}.image-caption{padding:10px 12px;color:var(--muted);font-size:12px;line-height:1.6}@media(max-width:640px){.wrap{padding:12px 10px 42px}.card{padding:16px;border-radius:16px}.prompt-row{display:grid}}
</style>
</head>
<body>
<canvas class="stars" id="stars"></canvas>
<div class="wrap">
  <div class="top"><div class="crest"><img src="assets/teachany-icon.png" alt="TeachAny"></div><div class="title"><h1>${safeTitle}互动挑战</h1><p>${book.grade}年级 · 自选书目 · ${escapeHtml(book.author || '未知')}</p></div><span class="badge" id="scoreBadge">积分 0</span></div>
  <div class="steps" id="steps"></div>
  <div class="card" id="scene"></div>
</div>
<script>
const DATA=${dataJson};
let state={idx:0,score:0,answered:false};
const $=s=>document.querySelector(s),scene=$('#scene'),steps=$('#steps'),scoreBadge=$('#scoreBadge');
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function renderSteps(){steps.innerHTML='';DATA.levels.forEach((_,i)=>{const d=document.createElement('div');d.className='step'+(i<state.idx?' done':'')+(i===state.idx?' cur':'');steps.appendChild(d)})}
function renderLevel(){renderSteps();scoreBadge.textContent='积分 '+state.score;state.answered=false;const lv=DATA.levels[state.idx];const hasImg=lv.img;const imgHtml=hasImg?'<div class="stage" id="stageBox"><div class="loading" id="stageLoading">正在生成场景插画…</div></div>':'';scene.innerHTML='<span class="scene-tag">'+lv.tag+'</span>'+imgHtml+'<p class="story">'+lv.story+'</p><div class="qbox"><p class="q">'+lv.q+'</p><p class="hint">'+lv.hint+'</p><div class="opts" id="opts"></div><div class="feedback" id="feedback"></div></div><div class="nav"><button class="btn btn-ghost" id="prevBtn" '+(state.idx===0?'style="display:none"':'')+'>&larr; 上一关</button><button class="btn btn-primary" id="nextBtn" disabled>'+(state.idx===DATA.levels.length-1?'查看结果 ✦':'下一关 &rarr;')+'</button></div>';if(hasImg)loadSceneImage(lv);const opts=$('#opts');shuffle(lv.opts.slice()).forEach(o=>{const b=document.createElement('button');b.className='opt';b.textContent=o.t;b.onclick=()=>answer(b,o,lv);opts.appendChild(b)});$('#nextBtn').onclick=()=>{state.idx===DATA.levels.length-1?showEnd():(state.idx++,renderLevel())};const prev=$('#prevBtn');if(prev)prev.onclick=()=>{state.idx--;renderLevel()}}
async function loadSceneImage(lv){var box=$('#stageBox'),loading=$('#stageLoading');if(!box)return;try{var url=await agnesImage(lv.img);var img=document.createElement('img');img.alt='场景插画';img.src=url;img.onload=function(){if(loading)loading.remove()};box.appendChild(img)}catch(e){if(loading)loading.textContent='插画加载失败，继续答题吧～'}}
function answer(btn,opt,lv){if(state.answered)return;state.answered=true;document.querySelectorAll('.opt').forEach(b=>{const o=lv.opts.find(x=>x.t===b.textContent);if(o&&o.c)b.classList.add('ok');else if(b===btn)b.classList.add('no')});const fb=$('#feedback');fb.innerHTML=(opt.c?'🌟 ':'💡 ')+lv.fb;fb.classList.add('show');if(opt.c){state.score++;scoreBadge.textContent='积分 '+state.score}$('#nextBtn').disabled=false}
function showEnd(){renderSteps();document.querySelectorAll('.step').forEach(s=>s.classList.add('done'));const full=state.score===DATA.levels.length;scene.innerHTML='<div class="end"><div style="font-size:46px">'+(full?'🏅':'📖')+'</div><h2>'+(full?'阅读徽章到手':'闯关完成')+'</h2><p class="blurb">你获得 <b style="color:var(--gold)">'+state.score+' / '+DATA.levels.length+'</b> 分。</p><div class="create"><h3>最后的创作任务：把阅读变成一张图</h3><p>请写一段图像提示词，包含"谁、在哪里、做什么、画面颜色或心情"。</p><div class="prompt-row"><input id="imagePrompt" value="《'+DATA.item.title+'》中我最想画的一幕，儿童绘本风格，温暖光线"><button class="btn btn-primary" id="imageBtn">生成我的阅读插画</button></div><div class="image-box" id="imageBox"><img id="imageResult" alt="阅读插画"><div class="image-caption" id="imageCaption"></div></div></div><div class="nav"><button class="btn btn-ghost" id="againBtn">再玩一次</button></div></div>';$('#againBtn').onclick=()=>{state={idx:0,score:0,answered:false};renderLevel()};$('#imageBtn').onclick=generateImage}
const AGNES_CFG={key:'${agnesKey}',base:'${agnesBase}',model:'${agnesModel}'};
async function agnesImage(prompt){const finalPrompt=prompt+'，儿童绘本插画，温暖光线，适合小学生阅读分享，无文字';const r=await fetch(AGNES_CFG.base+'/images/generations',{method:'POST',headers:{Authorization:'Bearer '+AGNES_CFG.key,'Content-Type':'application/json'},body:JSON.stringify({model:AGNES_CFG.model,prompt:finalPrompt,n:1,size:'1024x1024'})});if(!r.ok)throw new Error('生图失败 '+r.status);const d=await r.json();const item=(d.data&&d.data[0])||{};if(item.url)return item.url;if(item.b64_json)return 'data:image/png;base64,'+item.b64_json;throw new Error('生图返回为空')}
async function generateImage(){const input=$('#imagePrompt');const prompt=(input.value||'').trim();if(!prompt){input.focus();return}const img=$('#imageResult'),box=$('#imageBox'),caption=$('#imageCaption'),btn=$('#imageBtn');box.style.display='block';caption.textContent='正在生成阅读插画…';btn.disabled=true;try{img.src=await agnesImage(prompt);caption.textContent='提示词：'+prompt}catch(e){caption.textContent='生图失败：'+e.message}finally{btn.disabled=false}}
(function stars(){const c=$('#stars'),x=c.getContext('2d');function rs(){c.width=innerWidth;c.height=innerHeight}rs();addEventListener('resize',rs);const st=[];for(let i=0;i<80;i++)st.push({x:Math.random()*c.width,y:Math.random()*c.height,r:Math.random()*1.4+.3,a:Math.random()});(function draw(){x.clearRect(0,0,c.width,c.height);st.forEach(s=>{s.a+=(Math.random()-.5)*.05;if(s.a<.1)s.a=.1;if(s.a>1)s.a=1;x.beginPath();x.arc(s.x,s.y,s.r,0,7);x.fillStyle='rgba(231,198,107,'+(s.a*.65)+')';x.fill()});requestAnimationFrame(draw)})()})();
renderLevel();
</` + `script>
</body>
</html>`;
}

/* ─── 覆盖 updatePreview 以支持 blob URL ─── */
const _origUpdatePreview = updatePreview;
updatePreview = function() {
  const game = currentGame();
  if (!game) {
    els.previewFrame.removeAttribute('src');
    els.openLink.removeAttribute('href');
    els.practiceBtn.removeAttribute('href');
    return;
  }
  if (game.blobUrl) {
    els.previewFrame.src = game.url;
    els.openLink.href = game.url;
    els.practiceBtn.removeAttribute('href');
  } else {
    els.previewFrame.src = `./${game.url}`;
    els.openLink.href = `./${game.url}`;
    updatePracticeLink(game);
  }
};

init().catch((error) => {
  console.error(error);
  els.previewFrame.removeAttribute('src');
});

// 初始化自制游戏模块
initCustomGame();
