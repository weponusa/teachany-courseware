/**
 * TeachAny 课件中枢（Courseware Hub）v1.0
 *
 * 通用课件接口标准：聚合所有来源的课件，为知识图谱提供统一查询。
 *
 * 数据源：
 *   1. registry.json — 官方/社区课件（status: official / community）
 *   2. community/index.json — 社区共享课件（含 likes 字段）
 *   3. localStorage — 用户本地导入的课件（TeachAnyImporter）
 *
 * 核心逻辑：
 *   - 按 node_id 聚合所有课件
 *   - 多个课件时，按心标（likes）降序排列
 *   - 心标相同时，官方课件优先
 *
 * API：
 *   TeachAnyHub.getAllCoursesForNode(nodeId) → Array<UnifiedCourse>
 *   TeachAnyHub.getBestCourseForNode(nodeId) → UnifiedCourse | null
 *   TeachAnyHub.getNodeCourseCount(nodeId) → number
 *   TeachAnyHub.hasAnyCourseware(nodeId) → boolean
 *   TeachAnyHub.init() → Promise<void>
 */

/* ─── 常量 ────────────────────────────────────── */
const HUB_REGISTRY_URL = './registry.json';
const HUB_COMMUNITY_URL = './community/index.json';
const HUB_COURSEWARE_BASE_URL = 'https://www.teachany.cn';
const HUB_CACHE_KEY = 'teachany_hub_cache_v7'; // v7: auto-publish registry refresh
const HUB_CACHE_TTL = 15 * 60 * 1000; // 15 分钟

// 心标真值：Cloudflare Pages Functions + KV（teachany-community）
//   GET /api/like?ids=a,b,c → { ok, likes: { id: n } }
// 与画廊 unified-loader.js 读的是同一份计数，两边显示保持一致。
const HUB_LIKE_API = 'https://teachany-community.pages.dev/api/like';
const HUB_LIKE_BATCH = 200;      // 与后端 MAX_IDS_PER_QUERY 对齐
const HUB_LIKE_TIMEOUT = 4000;

function resolveCoursewareUrl(path) {
  if (!path) return HUB_COURSEWARE_BASE_URL + '/';
  if (/^https?:\/\//i.test(path)) return path;
  return HUB_COURSEWARE_BASE_URL + '/' + String(path).replace(/^\/+/, '').replace(/\/$/, '') + '/index.html';
}

/* ─── 内部状态 ────────────────────────────────── */
let _registryCourses = [];  // { id, node_id, name, subject, grade, likes, source, url, ... }
let _communityCourses = []; // 同上
let _initialized = false;
let _initPromise = null;

// node_id → UnifiedCourse[] 的索引
const _nodeIndex = new Map();

/* ─── 课件源类型 ──────────────────────────────── */
const SOURCE = {
  OFFICIAL: 'official',      // registry.json status=official
  COMMUNITY_REG: 'community_registry',  // registry.json status=community
  COMMUNITY_SHARED: 'community_shared', // community/index.json
  USER: 'user',              // localStorage 用户导入
};

const SOURCE_PRIORITY = {
  [SOURCE.OFFICIAL]: 0,
  [SOURCE.COMMUNITY_REG]: 1,
  [SOURCE.COMMUNITY_SHARED]: 2,
  [SOURCE.USER]: 3,
};

/* ─── 缓存 ────────────────────────────────────── */
function getHubCache() {
  try {
    const cached = localStorage.getItem(HUB_CACHE_KEY);
    if (!cached) return null;
    const { registry, community, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp > HUB_CACHE_TTL) {
      localStorage.removeItem(HUB_CACHE_KEY);
      return null;
    }
    if (!registry || !community) return null;
    return { registry, community };
  } catch {
    localStorage.removeItem(HUB_CACHE_KEY);
    return null;
  }
}

function setHubCache(registry, community) {
  try {
    localStorage.setItem(HUB_CACHE_KEY, JSON.stringify({
      registry, community, timestamp: Date.now()
    }));
  } catch {}
}

/* ─── JSON 加载 ───────────────────────────────── */
async function fetchJSON(url) {
  const resp = await fetch(url + '?t=' + Date.now(), { cache: 'no-store' });
  if (!resp.ok) throw new Error(`HTTP ${resp.status} for ${url}`);
  return resp.json();
}

/* ─── 初始化 ──────────────────────────────────── */
async function init() {
  if (_initialized) return;
  if (_initPromise) return _initPromise;

  _initPromise = _doInit();
  return _initPromise;
}

async function _doInit() {
  try {
    // 1. 尝试缓存
    const cached = getHubCache();
    let registryData, communityData;

    if (cached) {
      registryData = cached.registry;
      communityData = cached.community;
      console.log('[CoursewareHub] ✅ 使用缓存数据');
    } else {
      // 2. 并行加载两个数据源
      const [regResult, comResult] = await Promise.allSettled([
        fetchJSON(HUB_REGISTRY_URL),
        fetchJSON(HUB_COMMUNITY_URL),
      ]);
      const regOk = regResult.status === 'fulfilled';
      const comOk = comResult.status === 'fulfilled';
      registryData = regOk ? regResult.value : { courses: [] };
      communityData = comOk ? comResult.value : { courses: [] };
      // 仅在两个数据源都真正拿到、且 registry 非空时才写缓存并报成功。
      // 否则（部署窗口 / 网络抖动 / 5xx）会把「空索引」缓存 15 分钟，
      // 导致全站知识地图与知识树一律显示「无课件」。
      if (regOk && comOk && (registryData.courses || []).length > 0) {
        setHubCache(registryData, communityData);
        console.log('[CoursewareHub] ✅ 从服务器加载数据');
      } else {
        _initPromise = null;  // 允许下次进入页面时重试
        console.warn('[CoursewareHub] ⚠️ 数据源加载不完整，未写缓存，将自动重试：registry=' +
          regResult.status + ', community=' + comResult.status +
          ', registryCourses=' + ((registryData.courses || []).length));
      }
    }

    // 3. 标准化 registry 课件
    //    hosting === 'external-link' 表示课件托管在用户自己的知识库/服务器上，
    //    只有外链、没有本地目录。前端要把它和本地托管课件分开显示，所以把标识透传出来。
    _registryCourses = (registryData.courses || []).map(c => {
      const isExternal = c.hosting === 'external-link' || !!c.source_url;
      return {
        id: c.id,
        node_id: c.node_id || '',
        name: c.name || c.id,
        subject: c.subject || '',
        grade: c.grade || 0,
        emoji: c.emoji || '📚',
        likes: 0,
        source: c.status === 'official' ? SOURCE.OFFICIAL : SOURCE.COMMUNITY_REG,
        url: isExternal
          ? (c.source_url || c.download_url || '')
          : resolveCoursewareUrl(c.path || `community/${c.id}`),
        path: c.path || '',
        has_tts: c.has_tts || false,
        has_video: c.has_video || false,
        author: c.author || '',
        download_url: c.download_url || '',
        hosting: c.hosting || '',
        source_url: c.source_url || '',
        is_external: isExternal,
      };
    });

    // 4. 标准化 community 课件
    _communityCourses = (communityData.courses || []).map(c => {
      const isExternal = c.hosting === 'external-link' || !!c.source_url;
      return {
        id: c.id,
        node_id: c.node_id || '',
        name: c.name || c.id,
        subject: c.subject || '',
        grade: c.grade || 0,
        emoji: isExternal ? '🔗' : '🌐',
        likes: c.likes || 0,
        source: SOURCE.COMMUNITY_SHARED,
        url: c.download_url || resolveCoursewareUrl(c.path || `community/${c.id}`),
        path: c.path || '',
        has_tts: false,
        has_video: false,
        author: c.author || '',
        download_url: c.download_url || '',
        hosting: c.hosting || '',
        source_url: c.source_url || '',
        is_external: isExternal,
      };
    });

    // 5. 合并 likes：community/index.json 里的 likes 作初值（老数据兼容）
    const communityLikesMap = new Map();
    _communityCourses.forEach(c => {
      if (c.id && c.likes > 0) communityLikesMap.set(c.id, c.likes);
    });
    _registryCourses.forEach(c => {
      if (communityLikesMap.has(c.id)) {
        c.likes = communityLikesMap.get(c.id);
      }
    });

    // 6. 以服务端真实计数覆盖（拉取失败就保留上面的初值，不阻塞索引构建）
    //    注意：这里不再叠加 localStorage 的本地值——服务端才是唯一真值来源，
    //    叠加会让同一个数字被算两遍。
    const serverLikes = await fetchHubLikes(
      [..._registryCourses, ..._communityCourses].map(c => c.id)
    );
    if (serverLikes.size) {
      [..._registryCourses, ..._communityCourses].forEach(c => {
        if (c.id && serverLikes.has(c.id)) c.likes = serverLikes.get(c.id);
      });
      console.log(`[CoursewareHub] ✅ 服务端点赞数已合并: ${serverLikes.size} 条`);
    } else {
      console.warn('[CoursewareHub] ⚠️ 服务端点赞数拉取失败，沿用 community/index.json 初值');
    }

    // 7. 构建 node_id 索引
    _buildNodeIndex();

    _initialized = true;
    console.log(`[CoursewareHub] 索引完成: ${_nodeIndex.size} 个节点有课件, ` +
      `registry=${_registryCourses.length}, community=${_communityCourses.length}`);

  } catch (err) {
    console.error('[CoursewareHub] 初始化失败（未缓存，允许下次重试）:', err);
    _initPromise = null; // 原来置 _initialized=true 会把空索引锁死整页，改为允许重试
  }
}

/* ─── 心标真值（服务端计数） ──────────────────── */
async function fetchHubLikes(courseIds) {
  const ids = [...new Set((courseIds || []).filter(Boolean))];
  const out = new Map();
  if (!ids.length) return out;

  const batches = [];
  for (let i = 0; i < ids.length; i += HUB_LIKE_BATCH) batches.push(ids.slice(i, i + HUB_LIKE_BATCH));

  const results = await Promise.all(batches.map(async (group) => {
    let timer;
    try {
      const r = await Promise.race([
        fetch(`${HUB_LIKE_API}?ids=${encodeURIComponent(group.join(','))}`, { cache: 'no-store' }),
        new Promise((_, rej) => { timer = setTimeout(() => rej(new Error('timeout')), HUB_LIKE_TIMEOUT); }),
      ]);
      if (!r || !r.ok) return null;
      const data = await r.json();
      return (data && data.likes) || null;
    } catch {
      return null;
    } finally {
      clearTimeout(timer);
    }
  }));

  for (const likes of results) {
    if (!likes) continue;
    for (const [id, n] of Object.entries(likes)) out.set(id, Number(n) || 0);
  }
  return out;
}

/* ─── 构建索引 ────────────────────────────────── */
function _buildNodeIndex() {
  _nodeIndex.clear();

  // 合并所有课件
  const allCourses = [..._registryCourses, ..._communityCourses];

  // 去重：同一 id 只保留一个（优先保留 source 优先级高的）
  const seen = new Map(); // id → course
  for (const c of allCourses) {
    if (!c.node_id) continue;
    const existing = seen.get(c.id);
    if (!existing || (SOURCE_PRIORITY[c.source] || 9) < (SOURCE_PRIORITY[existing.source] || 9)) {
      seen.set(c.id, c);
    }
  }

  // 按 node_id 归类
  for (const c of seen.values()) {
    if (!c.node_id) continue;
    if (!_nodeIndex.has(c.node_id)) {
      _nodeIndex.set(c.node_id, []);
    }
    _nodeIndex.get(c.node_id).push(c);
  }

  // 添加用户导入课件
  _addUserCoursesToIndex();

  // 排序：每个 node_id 下的课件按 likes 降序 + 源优先级
  for (const [, courses] of _nodeIndex) {
    courses.sort((a, b) => {
      // 1. likes 降序
      if (b.likes !== a.likes) return b.likes - a.likes;
      // 2. 源优先级升序（official > community_registry > community_shared > user）
      return (SOURCE_PRIORITY[a.source] || 9) - (SOURCE_PRIORITY[b.source] || 9);
    });
  }
}

function _addUserCoursesToIndex() {
  if (!window.TeachAnyImporter) return;

  const userCourses = window.TeachAnyImporter.getUserCourses();
  for (const uc of userCourses) {
    const nodeId = uc.manifest?.node_id;
    if (!nodeId) continue;

    const userLikes = window.TeachAnyImporter.getCourseLikes(uc.id) || 0;
    const unified = {
      id: uc.id,
      node_id: nodeId,
      name: uc.manifest?.name || '用户课件',
      subject: uc.manifest?.subject || '',
      grade: uc.manifest?.grade || 0,
      emoji: uc.manifest?.emoji || '📂',
      likes: userLikes,
      source: SOURCE.USER,
      url: window.TeachAnyImporter.getCourseLaunchUrl(uc),
      path: '',
      has_tts: false,
      has_video: false,
      author: uc.manifest?.author || 'user',
      download_url: '',
    };

    // 别名映射：用户课件的 node_id 可能与树节点不一致
    const nodeIds = [nodeId];
    if (window.TeachAnyImporter.NODE_ID_ALIASES) {
      // 正向：manifest node_id → tree node id
      const forward = window.TeachAnyImporter.NODE_ID_ALIASES[nodeId];
      if (forward) nodeIds.push(...forward);
      // 反向：tree node id → manifest node_id
      for (const [mId, tIds] of Object.entries(window.TeachAnyImporter.NODE_ID_ALIASES)) {
        if (tIds.includes(nodeId)) nodeIds.push(mId);
      }
    }

    for (const nid of new Set(nodeIds)) {
      if (!_nodeIndex.has(nid)) {
        _nodeIndex.set(nid, []);
      }
      // 避免重复
      const existing = _nodeIndex.get(nid);
      if (!existing.some(c => c.id === unified.id)) {
        existing.push(unified);
      }
    }
  }
}

/* ─── 公共 API ────────────────────────────────── */

/**
 * 获取某节点的所有课件（已按 likes 降序排列）
 * @param {string} nodeId
 * @returns {Array<UnifiedCourse>}
 */
function getAllCoursesForNode(nodeId) {
  if (!nodeId) return [];
  return _nodeIndex.get(nodeId) || [];
}

/**
 * 获取某节点心标最高的课件
 * @param {string} nodeId
 * @returns {UnifiedCourse|null}
 */
function getBestCourseForNode(nodeId) {
  const courses = getAllCoursesForNode(nodeId);
  return courses.length > 0 ? courses[0] : null;
}

/**
 * 获取某节点的课件数量
 * @param {string} nodeId
 * @returns {number}
 */
function getNodeCourseCount(nodeId) {
  return getAllCoursesForNode(nodeId).length;
}

/**
 * 判断某节点是否有任何课件
 * @param {string} nodeId
 * @returns {boolean}
 */
function hasAnyCourseware(nodeId) {
  return getNodeCourseCount(nodeId) > 0;
}

/**
 * tree.json 的 courses[] 常为预留 id；仅当 registry/community 能解析时才视为真实课件。
 * @param {string[]} courses
 * @returns {UnifiedCourse[]}
 */
function getResolvableTreeCourses(courses) {
  if (!Array.isArray(courses) || !courses.length) return [];
  const out = [];
  const seen = new Set();
  courses.forEach((courseId) => {
    const id = typeof courseId === 'string' ? courseId.trim() : '';
    if (!id || seen.has(id)) return;
    const hit = getCourseById(id);
    if (hit) {
      seen.add(id);
      out.push(hit);
    }
  });
  return out;
}

function hasResolvableTreeCourses(courses) {
  return getResolvableTreeCourses(courses).length > 0;
}

/**
 * 手动刷新索引（用户导入新课件后调用）
 */
function refreshIndex() {
  _buildNodeIndex();
}

/**
 * 获取所有有课件的节点 ID 列表
 * @returns {string[]}
 */
function getAllCoveredNodeIds() {
  return Array.from(_nodeIndex.keys());
}

/**
 * 获取统计信息
 */
function getStats() {
  let totalCourses = 0;
  let nodesWithMultiple = 0;
  for (const [, courses] of _nodeIndex) {
    totalCourses += courses.length;
    if (courses.length > 1) nodesWithMultiple++;
  }
  return {
    coveredNodes: _nodeIndex.size,
    totalCourses,
    nodesWithMultiple,
    registryCourses: _registryCourses.length,
    communityCourses: _communityCourses.length,
  };
}

/* ─── 导出 ────────────────────────────────────── */

/**
 * v6.6: 按 course.id 查课件（返回包含 url 字段的 UnifiedCourse）
 * @param {string} courseId
 * @returns {UnifiedCourse|null}
 */
function getCourseById(courseId) {
  if (!courseId) return null;
  // 优先 registry（官方+社区都在）
  let hit = _registryCourses.find(c => c.id === courseId);
  if (hit) return hit;
  // 再查 community 下载链接
  hit = _communityCourses.find(c => c.id === courseId);
  if (hit) return hit;
  // 再查 _nodeIndex 里合并后的（含 user courses）
  for (const arr of _nodeIndex.values()) {
    hit = arr.find(c => c.id === courseId);
    if (hit) return hit;
  }
  return null;
}

/**
 * v7.15: 按关键词搜索课件（用于 PBL 外部节点匹配已有课件）
 * @param {string} keyword - 搜索关键词（如"锂离子电池技术"）
 * @param {number} [limit=5] - 最多返回条数
 * @returns {Array<UnifiedCourse>}
 */
function searchByKeyword(keyword, limit) {
  if (!keyword || typeof keyword !== 'string') return [];
  limit = limit || 5;
  const kw = keyword.toLowerCase().replace(/[·\s]+/g, '');
  const results = [];
  const seen = new Set();
  // 遍历 registry + community 课件，按名称模糊匹配
  for (const c of [..._registryCourses, ..._communityCourses]) {
    if (seen.has(c.id)) continue;
    const name = ((c.name || '') + (c.name_en || '') + (c.id || '')).toLowerCase().replace(/[·\s]+/g, '');
    // 关键词包含在名称中，或名称包含关键词
    if (name.includes(kw) || kw.includes(name.slice(0, Math.max(4, kw.length)))) {
      seen.add(c.id);
      results.push(c);
      if (results.length >= limit) break;
    }
  }
  return results;
}

window.TeachAnyHub = {
  init,
  getAllCoursesForNode,
  getBestCourseForNode,
  getNodeCourseCount,
  hasAnyCourseware,
  getResolvableTreeCourses,
  hasResolvableTreeCourses,
  getCourseById,  // v6.6: 新增
  searchByKeyword,  // v7.15: 新增
  refreshIndex,
  getAllCoveredNodeIds,
  getStats,
  SOURCE,
};
