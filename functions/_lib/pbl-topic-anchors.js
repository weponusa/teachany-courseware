/**
 * 题目语义 → 课标知识点召回锚点（地点/时代/主题驱动，不限项目类型）
 */

const PLACE_LEX = [
  { keys: /英国|英格兰|英伦|伦敦|剑桥|牛津|大不列颠/, id: 'uk', label: '英国', terms: ['英国', '英格兰', '大不列颠', '英伦', '西欧', '欧洲'], subjects: ['geography', 'history', 'english'], geoTerms: ['国家', '地形', '气候', '人文地理', '纬度', '海陆', '世界地形', '自然环境'] },
  { keys: /法国|法兰西|巴黎|卢浮宫/, id: 'fr', label: '法国', terms: ['法国', '法兰西', '西欧', '欧洲'], subjects: ['geography', 'history'], geoTerms: ['国家', '地形', '气候', '人文地理'] },
  { keys: /美国|北美|纽约|华盛顿|波士顿/, id: 'us', label: '美国', terms: ['美国', '北美', '美洲', '美利坚'], subjects: ['geography', 'history'], geoTerms: ['国家', '地形', '气候', '人文地理'] },
  { keys: /日本|东京|京都|大阪/, id: 'jp', label: '日本', terms: ['日本', '东亚', '岛国', '和服'], subjects: ['geography', 'history'], geoTerms: ['国家', '地形', '气候', '板块', '季风'] },
  { keys: /德国|柏林|慕尼黑/, id: 'de', label: '德国', terms: ['德国', '德意志', '欧洲'], subjects: ['geography', 'history'], geoTerms: ['国家', '地形', '气候'] },
  { keys: /意大利|罗马|威尼斯|佛罗伦萨/, id: 'it', label: '意大利', terms: ['意大利', '罗马', '欧洲', '地中海'], subjects: ['geography', 'history'], geoTerms: ['国家', '地形', '气候', '地中海'] },
  { keys: /埃及|金字塔|尼罗河|开罗/, id: 'eg', label: '埃及', terms: ['埃及', '尼罗河', '非洲', '金字塔', '文明'], subjects: ['geography', 'history'], geoTerms: ['河流', '地形', '气候', '沙漠'] },
  { keys: /印度|恒河|泰姬陵/, id: 'in', label: '印度', terms: ['印度', '南亚', '恒河', '文明'], subjects: ['geography', 'history'], geoTerms: ['国家', '地形', '气候', '季风'] },
  { keys: /澳大利亚|悉尼|袋鼠/, id: 'au', label: '澳大利亚', terms: ['澳大利亚', '澳洲', '大洋洲'], subjects: ['geography', 'history', 'biology'], geoTerms: ['国家', '地形', '气候', '大陆'] },
  { keys: /俄罗斯|莫斯科|西伯利亚/, id: 'ru', label: '俄罗斯', terms: ['俄罗斯', '西伯利亚', '欧洲', '亚洲'], subjects: ['geography', 'history'], geoTerms: ['国家', '地形', '气候', '纬度'] },
  { keys: /中国|华夏|北京|西安|江南|丝绸之路|长安|洛阳|故宫/, id: 'cn', label: '中国', terms: ['中国', '华夏', '中原', '江南', '黄河', '长江'], subjects: ['geography', 'history', 'chinese'], geoTerms: ['地形', '气候', '区域', '人文', '河流'] },
  { keys: /欧洲|欧盟|地中海|北欧|南欧|西欧|东欧/, id: 'europe', label: '欧洲', terms: ['欧洲', '西欧', '东欧', '北欧', '南欧', '地中海'], subjects: ['geography', 'history'], geoTerms: ['地形', '气候', '世界地形'] },
  { keys: /非洲|撒哈拉|东非|西非/, id: 'africa', label: '非洲', terms: ['非洲', '撒哈拉', '尼罗河', '刚果'], subjects: ['geography', 'history'], geoTerms: ['地形', '气候', '热带'] },
  { keys: /东南亚|新加坡|泰国|越南|马来西亚/, id: 'sea', label: '东南亚', terms: ['东南亚', '热带', '季风', '马来'], subjects: ['geography', 'history'], geoTerms: ['国家', '地形', '气候'] },
];

const PERIOD_LEX = [
  { keys: /中世纪|中古时期|中古时代|封建时代/, id: 'medieval', label: '中世纪', terms: ['中世纪', '中古', '封建', '骑士', '庄园', '教会', '领主', '欧洲', '庄园经济'], subjects: ['history'] },
  { keys: /文艺复兴/, id: 'renaissance', label: '文艺复兴', terms: ['文艺复兴', '人文主义', '宗教改革', '艺术', '科学革命'], subjects: ['history', 'chinese'] },
  { keys: /古代|先秦|秦汉|唐宋|明清|朝代|王朝|青铜|甲骨文/, id: 'ancient', label: '古代', terms: ['古代', '朝代', '王朝', '文明', '考古', '史料', '分封', '郡县'], subjects: ['history', 'chinese'] },
  { keys: /近代|工业革命|殖民|新航路|资本主义/, id: 'modern', label: '近代', terms: ['近代', '工业', '革命', '殖民', '资本主义', '资产阶级'], subjects: ['history', 'geography'] },
  { keys: /世界大战|二战|一战|冷战/, id: 'ww', label: '近现代战争', terms: ['战争', '世界', '冷战', '反法西斯'], subjects: ['history'] },
  { keys: /改革开放|新中国|社会主义建设/, id: 'cn-contemporary', label: '当代中国', terms: ['改革开放', '新中国', '社会主义', '现代化'], subjects: ['history', 'geography', 'chinese'] },
];

const THEME_LEX = [
  { keys: /研学|游学|考察|旅行|路线|目的地|field\s*trip/i, subjects: ['geography', 'history', 'chinese'], terms: ['区域', '人文', '遗址', '博物馆', '地形', '气候', '史迹', '交通'] },
  { keys: /博物馆|遗址|文物|古迹|遗产|史迹|考古/, subjects: ['history', 'chinese'], terms: ['文物', '考古', '文献', '史料', '遗产', '保护'] },
  { keys: /地形|气候|地貌|区位|地图|自然环境|地理景观/, subjects: ['geography'], terms: ['地形', '气候', '地图', '区域', '等高线', '景观'] },
  { keys: /莎士比亚|文学|戏剧|诗歌|诗人/, subjects: ['english', 'chinese', 'history'], terms: ['文学', '戏剧', '诗歌', '作家', '作品'] },
  { keys: /经济|贸易|市场|产业|商业/, subjects: ['math', 'geography', 'history', 'chinese'], terms: ['经济', '贸易', '市场', '产业', '统计'] },
  { keys: /生态|环境|污染|可持续|碳中和/, subjects: ['geography', 'biology', 'science', 'chemistry'], terms: ['生态', '环境', '污染', '资源', '循环'] },
];

function uniq(arr) {
  return [...new Set((arr || []).filter(Boolean))];
}

/**
 * @param {string} goal
 * @returns {{
 *   recallTerms: string[],
 *   subjects: string[],
 *   places: string[],
 *   periods: string[],
 *   hints: string,
 *   strong: boolean,
 * }}
 */
export function inferTopicKnowledgeAnchors(goal) {
  const g = String(goal || '').trim();
  const recallTerms = new Set();
  const subjects = new Set();
  const places = [];
  const periods = [];
  const hintParts = [];

  PLACE_LEX.forEach(entry => {
    if (!entry.keys.test(g)) return;
    places.push(entry.label);
    entry.terms.forEach(t => recallTerms.add(t));
    entry.subjects.forEach(s => subjects.add(s));
    if (entry.geoTerms) entry.geoTerms.forEach(t => recallTerms.add(t));
    hintParts.push(`${entry.label}→${entry.subjects.join('/')}`);
  });

  PERIOD_LEX.forEach(entry => {
    if (!entry.keys.test(g)) return;
    periods.push(entry.label);
    entry.terms.forEach(t => recallTerms.add(t));
    entry.subjects.forEach(s => subjects.add(s));
    hintParts.push(`${entry.label}史`);
  });

  THEME_LEX.forEach(entry => {
    if (!entry.keys.test(g)) return;
    (entry.terms || []).forEach(t => recallTerms.add(t));
    (entry.subjects || []).forEach(s => subjects.add(s));
  });

  const cjk = g.match(/[\u4e00-\u9fa5]{2,6}/g) || [];
  cjk.forEach(w => {
    if (!/^(设计|制作|开发|一个|关于|围绕|项目|方案|报告|策划|探究|调查)$/.test(w)) recallTerms.add(w);
  });

  const recallList = uniq([...recallTerms]).slice(0, 40);
  const subjectList = uniq([...subjects]);
  const strong = places.length > 0 || periods.length > 0 || recallList.length >= 4;

  return {
    recallTerms: recallList,
    subjects: subjectList,
    places,
    periods,
    hints: hintParts.length ? hintParts.join('；') : '',
    strong,
  };
}

/** @param {string} goal */
export function formatTopicAnchorHint(goal) {
  const a = inferTopicKnowledgeAnchors(goal);
  if (!a.strong) return '';
  const subj = a.subjects.length ? a.subjects.join('、') : '按题意';
  const terms = a.recallTerms.slice(0, 10).join('、');
  const hint = a.hints ? `｜语义：${a.hints}` : '';
  return `知识召回：优先匹配与「${terms}」相关的${subj}课标节点${hint}`;
}

/** 节点与锚点重叠分（供客户端评分） */
export function scoreNodeAgainstAnchors(node, anchors, nodeTextFn) {
  if (!anchors?.recallTerms?.length || !node) return 0;
  const text = typeof nodeTextFn === 'function'
    ? nodeTextFn(node)
    : `${node.name || ''} ${node.definition || node.description || ''}`;
  const name = String(node.name || '');
  let score = 0;
  anchors.recallTerms.forEach(t => {
    if (!t || t.length < 2) return;
    if (name.includes(t)) score += 8;
    else if (text.includes(t)) score += 4;
  });
  if (anchors.subjects?.includes(node.subject)) {
    const hit = anchors.recallTerms.some(t => t.length >= 2 && (name.includes(t) || text.includes(t)));
    if (hit) score += 6;
  }
  (anchors.places || []).forEach(place => {
    if (place.length >= 2 && (name.includes(place) || text.includes(place))) score += 10;
  });
  (anchors.periods || []).forEach(period => {
    if (period === '中世纪' && /中世纪|中古/.test(name + text)) score += 14;
    if (period === '文艺复兴' && /文艺复兴|人文主义/.test(name + text)) score += 14;
    if (period === '古代' && /古代|朝代|文明/.test(name)) score += 10;
    if (period === '近代' && /近代|工业|资产/.test(name)) score += 10;
  });
  if ((anchors.periods || []).includes('中世纪') && /工业革命|资产阶级革命|新民主主义|世界大战/.test(name)) score -= 12;
  return score;
}
