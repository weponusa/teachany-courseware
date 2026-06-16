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

init().catch((error) => {
  console.error(error);
  els.previewFrame.removeAttribute('src');
});
