/* 国内所在地 + 四个圈层 + 校外实践绑定。
 * Jev 可用时用独立 noul 改写分数；连不上时用本地规则，不挡住生成。
 * 不编造场馆名，也不写「去某区找个能看见课题词的地方」。
 * 课题要看出具体对象时，检索能看见它的博物馆、大学或设施；没有落在服务半径里的地点，就不加校外环节。
 */
(function (root) {
  const THRESHOLD = 0.2;
  const PLACE_JEV_THRESHOLD = 0.5;
  const RINGS = [
    { id: 'r0', label: '校园周边', radius: '0–1 km' },
    { id: 'r1', label: '街道', radius: '1–5 km' },
    { id: 'r2', label: '区县', radius: '5–15 km' },
    { id: 'r3', label: '城市当日', radius: '15–40 km' },
  ];
  const RING_INDEX = Object.fromEntries(RINGS.map((r, i) => [r.id, i]));

  /** 研究类型决定要不要出门、出门带回什么。场所类型不预置名单，检索词从课题对象里长出来。 */
  const RESEARCH_TYPES = [
    { id: 'observe', label: '观察记录', re: /观察|观测|察看|记录|探究/, evidence: '现场看见的现象' },
    { id: 'survey', label: '调查访谈', re: /调查|调研|访谈|问卷|走访|实地/, evidence: '现场计数或询问得到的记录' },
    { id: 'sample', label: '采样检测', re: /采样|测量|检测|测定|实验|读数|采集|测算/, evidence: '读数、样本或对照' },
    { id: 'visit', label: '实地考察', re: /参观|研学|考察/, evidence: '对照实物写下的笔记' },
    { id: 'make', label: '对照制作', re: /制作|搭建|模型|测绘/, evidence: '真实参照的尺寸或材料' },
  ];
  const DESK_ONLY = /写诗|诗集|作文|读后感|购车|决策对比|演讲稿/;
  const STRIP = /调查|调研|观察|观测|察看|记录|采样|测量|检测|测定|实验(?!室)|读数|采集|测算|探究|参观|研学|考察|访谈|问卷|走访|实地|制作|搭建|模型|测绘|本地|家乡|我们|一个|进行|研究|项目|学生|如何|怎么|以及|并且|完成|设计|撰写|提出|分析|校园|一组|现代|主题|可以|通过|围绕|关于|相关/g;

  const LEAD = /^(在|对|把|将|从|为|和|与|及|的|了|是|有|其|该|本|一处|一次|一组|一家|一件|一份|一项|一些|不同)+/;
  const TAIL = /(在|对|把|将|从|为|和|与|及|的|了|是|有|其|该|本|并)+$/;
  const KEEP_TAIL = ['开放日'];
  const SKIP_GRAM = new Set(['方式', '公共', '不同', '一处', '一次', '一组', '本地', '我们', '什么', '为什么', '怎么', '怎样', '如何', '会飞', '那么', '未来', '能源', '清洁', '科学', '生态', '生活', '原理', '效率', '应用', '前景']);
  const NOT_A_PLACE = /什么|为什么|怎么|怎样|如何|会飞|那么|哪儿|哪里|未来|能源|清洁|科学|生态/;

  function topicPieces(part) {
    return String(part || '')
      .split(/[在和与及的并了是有其该本为从把将对]+/)
      .flatMap(piece => {
        let rest = piece.replace(LEAD, '').replace(TAIL, '').trim();
        const peeled = [];
        KEEP_TAIL.forEach(tail => {
          if (rest.endsWith(tail) && rest.length > tail.length) {
            peeled.push(tail);
            rest = rest.slice(0, -tail.length);
          }
        });
        return [rest, ...peeled];
      })
      .map(piece => piece.trim())
      .filter(piece => piece.length >= 2 && piece.length <= 8 && !/^写/.test(piece));
  }

  function derivePlaceSearch(text) {
    const src = String(text || '');
    const withoutDesk = src.replace(DESK_ONLY, ' ');
    const researchTypes = RESEARCH_TYPES.filter(item => item.re.test(withoutDesk));
    if (!researchTypes.length) {
      return { researchTypes: [], evidence: [], topics: [], queries: [] };
    }
    const topics = [];
    withoutDesk.replace(STRIP, ' ').split(/[^\u4e00-\u9fa5a-zA-Z0-9]+/).forEach(raw => {
      topicPieces(raw).forEach(part => {
        topics.push(part);
        if (/^[\u4e00-\u9fa5]{4}$/.test(part) || /^[\u4e00-\u9fa5]{6}$/.test(part)) {
          for (let i = 0; i + 2 <= part.length; i += 2) {
            const gram = part.slice(i, i + 2);
            if (!SKIP_GRAM.has(gram)) topics.push(gram);
          }
        }
      });
    });
    const unique = [...new Set(topics)].filter(term => term.length >= 2 && !SKIP_GRAM.has(term) && !NOT_A_PLACE.test(term)).slice(0, 6);
    if (!unique.length) return { researchTypes, evidence: researchTypes.map(item => item.evidence), topics: [], queries: [] };
    return {
      researchTypes,
      evidence: researchTypes.map(item => item.evidence),
      topics: unique,
      queries: unique.map(term => ({
        id: term,
        label: term,
        queries: [term],
        researchType: researchTypes.map(item => item.label).join('、'),
      })),
    };
  }

  function deriveIntents(text) {
    const found = derivePlaceSearch(text);
    return {
      specific: found.topics.length > 0,
      topics: found.topics,
      evidence: found.evidence,
      researchTypes: found.researchTypes,
      ids: found.researchTypes.map(item => item.id),
      categories: new Set(found.topics),
    };
  }

  /** 课题对象 → 能看见它的场所。检索词是场所，不是「什么、会飞」这类问句碎片。 */
  const SEE_AT = [
    { re: /氢能|氢气|燃料电池|加氢/, stem: /氢|燃料电池|加氢/, terms: ['加氢站', '氢能', '燃料电池'] },
    { re: /飞机|航空|机翼|升力|火箭|航天|飞行/, stem: /航空|航天|飞机|机场/, terms: ['航空航天博物馆', '航空航天大学', '中国航空博物馆', '航空博物馆'] },
    { re: /垃圾|废弃|废旧|回收|变废|填埋|再生资源|分类投放|扔掉/, stem: /回收|分类|填埋|转运|再生|垃圾|焚烧/, terms: ['再生资源回收', '垃圾分类', '填埋场', '垃圾转运'] },
    { re: /天文|星空|星座|行星|月球|月相|月亮|星星/, stem: /天文/, terms: ['天文馆', '天文台'] },
    { re: /恐龙|化石|矿物|地质/, stem: /自然|地质|化石|恐龙/, terms: ['自然博物馆', '地质博物馆'] },
    { re: /植物|绿植|树木|花园/, stem: /植物/, terms: ['植物园'] },
    { re: /动物|昆虫|鸟类|动物园/, stem: /动物|昆虫|鸟/, terms: ['动物园'] },
    { re: /河|江|湖|水质|湿地|潮汐/, stem: /河|江|湖|湿地|渠|溪/, terms: ['湿地公园', '河'] },
    { re: /古建|斗拱|遗址|文物|古迹/, stem: /博物|古迹|遗址|文保|塔/, terms: ['博物馆'] },
  ];

  function withCity(terms, city) {
    const prefixed = [];
    const plain = [];
    terms.forEach(term => {
      if (city && /博物馆|大学|天文馆|植物园|动物园/.test(term) && !/^中国|^国家/.test(term)) prefixed.push(city + term);
      plain.push(term);
    });
    return [...new Set(prefixed.concat(plain))].slice(0, 4);
  }

  function seeAt(text) {
    return SEE_AT.find(rule => rule.re.test(String(text || ''))) || null;
  }

  function searchTerms(text, place) {
    const src = String(text || '');
    const city = String((place && (place.city || place.province)) || '').replace(/市$/, '');
    const rule = seeAt(src);
    if (rule) {
      const extra = derivePlaceSearch(src).topics.filter(term => rule.stem.test(term) && term.length <= 4);
      return withCity(rule.terms.concat(extra), city);
    }
    return derivePlaceSearch(src).topics;
  }

  function poiQueries(text) {
    return searchTerms(text).map(term => ({ id: term, label: term, queries: [term] }));
  }

  function topicHits(term, blob) {
    if (!term || !blob) return false;
    if (blob.includes(term)) return true;
    if (term.length < 2) return false;
    for (let i = 0; i + 2 <= term.length; i += 1) {
      const gram = term.slice(i, i + 2);
      if (/^[\u4e00-\u9fa5]{2}$/.test(gram) && blob.includes(gram)) return true;
    }
    return false;
  }

  function localNoul(text, venue, intents) {
    const topics = (intents && intents.topics) || deriveIntents(text).topics;
    if (!topics.length) return 0.09;
    const blob = `${venue.name || ''} ${venue.canDo || ''} ${venue.category || ''}`;
    return topics.some(term => topicHits(term, blob)) ? 0.74 : 0.1;
  }

  /** 公开场所名录。districtCode / cityCode 与 cn-pca 一致。没有把握的不写进名录。 */
  const VENUES = [
    { id: 'hd-wanquan', name: '海淀公园万泉河河段', cityCode: '1101', districtCode: '110108', category: 'river', ring: 'r1', canDo: '在公开河岸观察水色、气味，用试纸读 pH，不下水', evidence: '3 个点的读数、河岸照片、排污口位置草图' },
    { id: 'hd-cuihu', name: '翠湖国家城市湿地公园', cityCode: '1101', districtCode: '110108', category: 'wetland', ring: 'r2', canDo: '沿公开步道记录湿地植物和水质外观', evidence: '观察记录表和一张步道路线图' },
    { id: 'hd-garden', name: '国家植物园', cityCode: '1101', districtCode: '110108', category: 'park', ring: 'r2', canDo: '观察植物形态并做分类记录', evidence: '至少 5 种植物的图文记录' },
    { id: 'cy-cst', name: '中国科学技术馆', cityCode: '1101', districtCode: '110105', category: 'science', ring: 'r2', canDo: '对照展项完成一次可记录的观察或测量', evidence: '展项名称、观察到的现象、和项目问题的对照' },
    { id: 'xc-planet', name: '北京天文馆', cityCode: '1101', districtCode: '110102', category: 'planetarium', ring: 'r2', canDo: '记录一场天象或展项里的星体运动', evidence: '观察笔记和一张自己画的位置草图' },
    { id: 'sz-twin', name: '罗汉院双塔', cityCode: '3205', districtCode: '320508', category: 'heritage', ring: 'r1', canDo: '在塔外估计斗拱层数和出跳，画比例草图，不进入未开放院落', evidence: '草图、层数记录、和模型尺寸的对照' },
    { id: 'sz-museum', name: '苏州博物馆', cityCode: '3205', districtCode: '320508', category: 'museum', ring: 'r2', canDo: '参观展陈并摘录与建筑相关的一件实物', evidence: '一件展品的摘录，不能代替外观测绘' },
    { id: 'sh-stm', name: '上海科技馆', cityCode: '3101', districtCode: '310115', category: 'science', ring: 'r2', canDo: '对照展项完成一次可记录的观察', evidence: '展项现象和项目问题的对照表' },
    { id: 'gz-gsc', name: '广东科学中心', cityCode: '4401', districtCode: '440113', category: 'science', ring: 'r2', canDo: '对照展项完成一次可记录的观察或测量', evidence: '展项现象和项目问题的对照表' },
    { id: 'szn-bay', name: '深圳湾公园', cityCode: '4403', districtCode: '440305', category: 'park', ring: 'r1', canDo: '沿公开岸线观察湿地、鸟类或潮汐痕迹', evidence: '观察记录和一张岸线草图' },
  ];

  function regions() {
    return root.CN_PCA || [];
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  function provinceOf(code) {
    return regions().find(p => p.code === code) || null;
  }

  function citiesOf(province) {
    return (province && province.children) || [];
  }

  function isMunicipality(province) {
    const cities = citiesOf(province);
    return cities.length === 1 && cities[0].name === '市辖区';
  }

  function districtsOf(city) {
    return (city && city.children) || [];
  }

  let districtRows = null;
  function districtIndex() {
    if (districtRows) return districtRows;
    districtRows = [];
    regions().forEach(prov => {
      citiesOf(prov).forEach(city => {
        const cityName = city.name === '市辖区' ? prov.name : city.name;
        districtsOf(city).forEach(dist => {
          districtRows.push({
            provinceCode: prov.code,
            province: prov.name,
            cityCode: city.code,
            city: cityName,
            districtCode: dist.code,
            district: dist.name,
            label: cityName === prov.name ? `${prov.name} ${dist.name}` : `${prov.name} ${cityName} ${dist.name}`,
          });
        });
      });
    });
    return districtRows;
  }

  function searchDistricts(text) {
    const q = String(text || '').replace(/\s+/g, '');
    if (q.length < 2) return [];
    const scored = [];
    districtIndex().forEach(row => {
      const name = row.district;
      let score = 0;
      if (name === q || name === `${q}区` || name === `${q}县` || name === `${q}市`) score = 5;
      else if (name.startsWith(q)) score = 4;
      else if (name.includes(q)) score = 3;
      else if (`${row.city}${name}`.includes(q) || `${row.province}${name}`.includes(q)) score = 2;
      if (score) scored.push({ ...row, score });
    });
    scored.sort((a, b) => b.score - a.score || a.label.length - b.label.length);
    return scored.slice(0, 8);
  }

  function haversineKm(lon1, lat1, lon2, lat2) {
    const rad = Math.PI / 180;
    const dLat = (lat2 - lat1) * rad;
    const dLon = (lon2 - lon1) * rad;
    const a = Math.sin(dLat / 2) ** 2
      + Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLon / 2) ** 2;
    return 2 * 6371 * Math.asin(Math.min(1, Math.sqrt(a)));
  }

  function ringFromKm(km) {
    if (km == null || !isFinite(km)) return null;
    if (km <= 1) return 'r0';
    if (km <= 5) return 'r1';
    if (km <= 15) return 'r2';
    if (km <= 40) return 'r3';
    return null;
  }

  function formatDistance(km) {
    if (km == null || !isFinite(km)) return '';
    if (km < 1) return `${Math.max(50, Math.round(km * 1000 / 10) * 10)} m`;
    if (km < 10) return `${km.toFixed(1)} km`;
    return `${Math.round(km)} km`;
  }

  /** 设施级别越低，服务范围越小。超出服务半径的网点不推荐。
   *  门前点位 2 km，街道网点 5 km，区县设施 15 km，城市设施 40 km。
   *  河、古迹这类研究对象本身不按网点半径卡，只受当日 40 km 限制。 */
  function serviceRadiusKm(name, tags) {
    const text = `${name || ''} ${(tags && tags.amenity) || ''} ${(tags && tags.landuse) || ''} ${(tags && tags.tourism) || ''}`;
    if (/填埋|焚烧|landfill|waste_disposal|国家级|省级|全市|枢纽/.test(text)) return 40;
    if (/博物馆|科技馆|天文馆|大学|高校|景区|植物园|湿地公园|风景名胜/.test(text) && !/社区/.test(text)) return 40;
    if (/转运|中转|分拣中心|回收中心|处理中心|waste_transfer/.test(text)) return 15;
    if (/点|亭|驿站|社区|网格|投放|便民/.test(text)) return 2;
    if (/回收|分类|recycling|加油站|加氢站|菜市|卫生服务/.test(text)) return 5;
    if (/氢能|燃料电池/.test(text)) return 15;
    if (/公园|文化馆|图书馆|体育馆|展览馆/.test(text)) return 15;
    return null;
  }

  function withinService(venue) {
    if (!venue || venue.distanceKm == null) return true;
    const limit = venue.serviceLimitKm != null
      ? venue.serviceLimitKm
      : serviceRadiusKm(venue.name, { amenity: venue.category });
    if (limit == null) return true;
    return venue.distanceKm <= limit;
  }

  function mapFilters(topics) {
    const blob = (topics || []).join('');
    const filters = [];
    const names = (topics || []).filter(term => /[\u4e00-\u9fa5]/.test(term) && term.length >= 2).slice(0, 4);
    const pattern = [];
    names.forEach(term => {
      pattern.push(term);
      const stem = term.match(/河|江|湖|溪|渠/);
      if (stem) pattern.push(stem[0]);
    });
    if (pattern.length) filters.push({ name: [...new Set(pattern)].slice(0, 5).join('|') });
    if (/公园|景区|绿地/.test(blob)) filters.push({ park: true });
    if (/博物馆|科技馆|天文馆|展览/.test(blob)) filters.push({ museum: true });
    if (/加油站/.test(blob)) filters.push({ fuel: true });
    if (/工厂|产业园|车间/.test(blob)) filters.push({ industrial: true });
    if (/实验室|大学|高校/.test(blob)) filters.push({ university: true });
    if (/村落|古建|斗拱|文保|遗址|古迹/.test(blob)) filters.push({ historic: true });
    if (/农田|作物|水利/.test(blob)) filters.push({ farm: true });
    if (/垃圾|回收|填埋|再生|转运/.test(blob)) filters.push({ waste: true });
    return filters;
  }

  function usablePlace(tags, topics) {
    const name = tags && tags.name;
    if (!name || String(name).length < 2) return false;
    const blob = (topics || []).join('');
    if (tags.highway && !/路|街|交通|站/.test(blob)) return false;
    if (tags.place && /city|town|village|hamlet|suburb/.test(tags.place) && !/村|镇/.test(blob)) return false;
    if (tags.landuse === 'residential' || tags.landuse === 'construction') return false;
    return true;
  }

  function fitsTopic(tags, topics) {
    const wanted = (topics || []).join('');
    const name = String((tags && tags.name) || '');
    if (/小学|中学|幼儿园/.test(name) || (tags && tags.amenity === 'school')) return false;
    const rule = SEE_AT.find(item => item.stem.test(wanted) || item.re.test(wanted));
    if (!rule) return true;
    return rule.stem.test(name);
  }

  function visitAction(name, tags) {
    const blob = `${name} ${tags.amenity || ''} ${tags.landuse || ''}`;
    if (/填埋|焚烧|处置|landfill|waste_disposal/.test(blob)) {
      return `在「${name}」的开放参观或外围观察垃圾最终去向，不进入填埋作业面`;
    }
    if (/回收|分类|转运|再生|垃圾|recycling|waste_transfer/.test(blob)) {
      return `在「${name}」的对外开放区域记录垃圾怎样被分类、回收或运走，不进入作业区`;
    }
    if (/航空|航天|飞机/.test(blob) && /博物馆/.test(blob)) {
      return `在「${name}」按开放路线看真实飞机或航空器，对照机翼做记录，不进入未开放库区`;
    }
    if (/航空|航天/.test(blob) && /大学|学院/.test(blob)) {
      return `在「${name}」的校园开放区域或校内博物馆参观，只停留在允许进入的公共区域`;
    }
    return `到「${name}」完成和课题对应的现场记录，只停留在对外开放区域`;
  }

  function specificName(tags) {
    const name = String(tags.name || '');
    const street = tags['addr:street'] || tags.street || '';
    if (street && !name.includes(street)) return `${name}（${street}）`;
    return name;
  }

  function recall(place) {
    if (!place || !place.districtCode) return [];
    const out = [];
    VENUES.forEach(venue => {
      let ringId = null;
      if (venue.districtCode === place.districtCode) ringId = venue.ring || 'r2';
      else if (venue.cityCode && venue.cityCode === place.cityCode) ringId = 'r3';
      if (!ringId) return;
      out.push({
        ...venue,
        ringId,
        ringLabel: (RINGS.find(r => r.id === ringId) || {}).label || ringId,
        jevCandidate: `${venue.name}（${(RINGS.find(r => r.id === ringId) || {}).label || ringId}，${venue.category}）：${venue.canDo}`,
      });
    });
    return out;
  }

  function bind(place, goal, mode, scored) {
    const intents = deriveIntents(goal);
    const rule = seeAt(goal);
    if (!intents.topics.length && !searchTerms(goal, place).length) return null;
    const source = scored === undefined ? recall(place) : scored;
    const candidates = source.map(venue => ({
      ...venue,
      noul: venue.noul == null ? localNoul(goal, venue, intents, mode) : venue.noul,
    }));
    const dropped = [];
    for (const ring of RINGS) {
      const pool = candidates.filter(venue => venue.ringId === ring.id);
      if (!pool.length) continue;
      const kept = [];
      pool.forEach(venue => {
        if (venue.noul != null && venue.noul < (venue.jevSource === 'jev' ? PLACE_JEV_THRESHOLD : THRESHOLD)) dropped.push(venue);
        else if (!withinService(venue)) dropped.push(venue);
        else if (rule && !rule.stem.test(venue.name || '')) dropped.push(venue);
        else kept.push(venue);
      });
      if (!kept.length) continue;
      kept.sort((a, b) => {
        if (a.distanceKm != null && b.distanceKm != null && a.distanceKm !== b.distanceKm) return a.distanceKm - b.distanceKm;
        return (b.noul || 0) - (a.noul || 0);
      });
      const best = kept[0];
      return {
        status: 'bound',
        ringId: ring.id,
        ringLabel: ring.label,
        name: best.name,
        category: best.category,
        action: `成人陪同，${best.canDo}。`,
        evidence: best.evidence,
        adultRequired: true,
        sameDay: true,
        jevSource: best.jevSource || 'local',
        noul: best.noul,
        venueId: best.id,
        distanceKm: best.distanceKm == null ? null : best.distanceKm,
        distanceText: formatDistance(best.distanceKm),
        originLabel: place.landmark || '',
        also: candidates
          .filter(venue => venue.name !== best.name && venue.noul != null && venue.noul >= (venue.jevSource === 'jev' ? PLACE_JEV_THRESHOLD : THRESHOLD) && withinService(venue) && (!rule || rule.stem.test(venue.name || '')))
          .sort((a, b) => a.distanceKm - b.distanceKm)
          .slice(0, 3)
          .map(venue => ({ name: venue.name, distanceText: formatDistance(venue.distanceKm), ringLabel: venue.ringLabel })),
        dropped: dropped.map(venue => ({
          name: venue.name,
          ringLabel: venue.ringLabel,
          noul: venue.noul,
          distanceText: formatDistance(venue.distanceKm),
        })),
        candidates,
      };
    }
    return null;
  }

  function resolve(opts) {
    const place = opts && opts.place;
    const goal = (opts && opts.goal) || '';
    const mode = (opts && opts.mode) || 'pbl';
    if (!place || !place.districtCode || !String(place.landmark || '').trim()) return null;
    const bound = bind(place, goal, mode, opts && opts.candidates);
    if (!bound) return null;
    const bits = [];
    if (place.province) bits.push(place.province);
    if (place.city && place.city !== place.province) bits.push(place.city);
    if (place.district) bits.push(place.district);
    if (place.landmark) bits.push(place.landmark);
    bound.placeLabel = bits.join('');
    bound.originLabel = place.landmark;
    bound.mode = mode;
    bound._place = place;
    if (opts && opts.center) bound.center = opts.center;
    return bound;
  }

  const SEARCH_RADII = [1000, 5000, 15000, 40000];

  function fetchJson(url, options, timeoutMs) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs || 12000);
    const headers = { Accept: 'application/json' };
    if (typeof document === 'undefined') headers['User-Agent'] = 'TeachAnyPlace/1.0';
    return fetch(url, { ...(options || {}), headers: { ...headers, ...((options && options.headers) || {}) }, signal: controller.signal })
      .then(resp => {
        if (!resp.ok) throw new Error(String(resp.status));
        return resp.json();
      })
      .finally(() => clearTimeout(timer));
  }

  async function geocodeCenter(place) {
    const district = place.district || '';
    const city = place.city && place.city !== place.province ? place.city : '';
    const cityShort = (city || '').replace(/市$/, '');
    const queries = [
      `${city}${place.landmark}`,
      `${cityShort}${place.landmark}`,
      `${district}${place.landmark}`,
      `${city}${district}${place.landmark}`,
    ];
    for (const q of queries) {
      if (!q) continue;
      let data = null;
      try {
        data = await fetchJson(`https://photon.komoot.io/api/?limit=5&q=${encodeURIComponent(q)}`, null, 8000);
      } catch (e) {
        data = null;
      }
      const features = (data && data.features) || [];
      const ranked = features.map(feature => {
        const props = feature.properties || {};
        const coords = (feature.geometry && feature.geometry.coordinates) || [];
        const blob = `${props.name || ''}${props.city || ''}${props.state || ''}${props.district || ''}${props.county || ''}${props.street || ''}`;
        let score = 0;
        const stem = district.replace(/[区县市]$/, '');
        if (stem && blob.includes(stem)) score += 3;
        if (city && blob.includes(city.replace(/市$/, ''))) score += 2;
        const kind = String(place.landmark || '').match(/小学|中学|学校|幼儿园/);
        if (kind && props.name && String(props.name).includes(kind[0])) score += 4;
        if (kind && props.name && !String(props.name).includes(kind[0])) score -= 4;
        if (props.name && place.landmark && String(props.name).includes(String(place.landmark).slice(0, 4))) score += 2;
        return {
          lon: coords[0],
          lat: coords[1],
          name: props.name || place.landmark,
          street: props.street || '',
          score,
        };
      }).filter(item => item.lat != null && item.lon != null && item.score > 0);
      ranked.sort((a, b) => b.score - a.score);
      if (ranked[0]) return ranked[0];
    }
    try {
      const q = `${place.city || place.province || ''}${place.district || ''}${place.landmark}`;
      const rows = await fetchJson(`https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&countrycodes=cn&q=${encodeURIComponent(q)}`, null, 8000);
      const hit = (Array.isArray(rows) ? rows : []).find(row => {
        const blob = `${row.display_name || ''}`;
        const stem = String(place.district || '').replace(/[区县市]$/, '');
        return !stem || blob.includes(stem);
      });
      if (hit) return { lon: Number(hit.lon), lat: Number(hit.lat), name: place.landmark, street: '', score: 1 };
    } catch (e) { /* 地理编码失败就不再编造圆心 */ }
    return null;
  }

  function venuesFromElements(elements, center, topics) {
    const byName = new Map();
    (elements || []).forEach(el => {
      const tags = el.tags || {};
      if (!usablePlace(tags, topics)) return;
      if (!fitsTopic(tags, topics)) return;
      const lat = el.lat != null ? el.lat : (el.center && el.center.lat);
      const lon = el.lon != null ? el.lon : (el.center && el.center.lon);
      if (lat == null || lon == null) return;
      const distanceKm = haversineKm(center.lon, center.lat, lon, lat);
      const serviceLimitKm = serviceRadiusKm(tags.name, tags);
      if (serviceLimitKm != null && distanceKm > serviceLimitKm) return;
      const ringId = ringFromKm(distanceKm);
      if (!ringId) return;
      const name = specificName(tags);
      const prev = byName.get(name);
      if (prev && prev.distanceKm <= distanceKm) return;
      const ring = RINGS.find(item => item.id === ringId) || {};
      byName.set(name, {
        id: `map-${name}`,
        name,
        category: tags.waterway || tags.leisure || tags.tourism || tags.amenity || tags.historic || tags.natural || 'place',
        ringId,
        ringLabel: ring.label || ringId,
        distanceKm,
        serviceLimitKm,
        noul: 0.74,
        jevSource: 'map',
        canDo: visitAction(name, tags),
        evidence: '地点名称、距离学校的记录、现场看到的现象',
        jevCandidate: [
          name,
          `距${center.label || '学校'} ${formatDistance(distanceKm)}`,
          `在开放区域要看见的对象必须就是课题本身，不能只是地名里有相同的字`,
          visitAction(name, tags),
        ].join('。'),
        lat,
        lon,
        rank: (tags.waterway || tags.natural === 'water' || tags.leisure === 'park' || tags.tourism || tags.amenity || tags.historic) ? 2 : 1,
      });
    });
    let venues = [...byName.values()];
    if (venues.some(venue => venue.rank > 1)) venues = venues.filter(venue => venue.rank > 1);
    return venues.sort((a, b) => a.distanceKm - b.distanceKm).slice(0, 8);
  }

  async function overpassAround(center, radius, filters) {
    const lines = [];
    filters.forEach(filter => {
      const around = `around:${radius},${center.lat},${center.lon}`;
      if (filter.name) {
        lines.push(`way(${around})["name"~"${filter.name}"];`);
        lines.push(`node(${around})["name"~"${filter.name}"];`);
      }
      if (filter.park) lines.push(`nwr(${around})["leisure"="park"]["name"];`);
      if (filter.museum) lines.push(`nwr(${around})["tourism"="museum"]["name"];`);
      if (filter.fuel) lines.push(`nwr(${around})["amenity"="fuel"]["name"];`);
      if (filter.industrial) lines.push(`nwr(${around})["landuse"="industrial"]["name"];`);
      if (filter.university) lines.push(`nwr(${around})["amenity"="university"]["name"];`);
      if (filter.historic) lines.push(`nwr(${around})["historic"]["name"];`);
      if (filter.farm) lines.push(`nwr(${around})["landuse"="farmland"]["name"];`);
      if (filter.waste) {
        lines.push(`node(${around})["amenity"="recycling"]["name"];`);
        lines.push(`node(${around})["amenity"="waste_transfer_station"]["name"];`);
      }
    });
    if (!lines.length) return [];
    const query = `[out:json][timeout:12];(${lines.join('')});out center 12;`;
    const data = await fetchJson('https://lz4.overpass-api.de/api/interpreter', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: `data=${encodeURIComponent(query)}`,
    }, 8000);
    return (data && data.elements) || [];
  }

  async function photonAround(center, radiusKm, topics) {
    const latPad = radiusKm / 111;
    const lonPad = radiusKm / (111 * Math.cos(center.lat * Math.PI / 180) || 1);
    const bbox = [center.lon - lonPad, center.lat - latPad, center.lon + lonPad, center.lat + latPad].join(',');
    const elements = [];
    for (const term of (topics || []).slice(0, 4)) {
      let data = null;
      try {
        data = await fetchJson(`https://photon.komoot.io/api/?${new URLSearchParams({
          q: term, lat: String(center.lat), lon: String(center.lon), limit: '6', location_bias_scale: '1', bbox,
        })}`, null, 8000);
      } catch (e) {
        data = null;
      }
      ((data && data.features) || []).forEach(feature => {
        const props = feature.properties || {};
        const coords = (feature.geometry && feature.geometry.coordinates) || [];
        const key = props.osm_key;
        const value = props.osm_value;
        const tags = { name: props.name, street: props.street || '' };
        if (key && value) tags[key] = value;
        elements.push({ lat: coords[1], lon: coords[0], tags });
      });
    }
    return elements;
  }

  async function searchAround(center, topics) {
    const filters = mapFilters(topics);
    const collect = async radius => {
      let elements = [];
      try {
        elements = await overpassAround(center, radius, filters);
      } catch (e) {
        if (String(e && e.message) === '429') throw e;
        elements = [];
      }
      return venuesFromElements(elements, center, topics).filter(venue => venue.distanceKm * 1000 <= radius);
    };
    let weak = [];
    for (const radius of [2000, 8000]) {
      let venues = [];
      try {
        venues = await collect(radius);
      } catch (e) {
        break;
      }
      const strong = venues.filter(venue => venue.rank > 1);
      if (strong.length) return strong;
      if (!weak.length && venues.length) weak = venues;
    }
    if (weak.length) return weak;
    try {
      const pattern = ((filters.find(filter => filter.name) || {}).name || '').split('|').filter(Boolean);
      const elements = await photonAround(center, 40, pattern.length ? pattern : topics);
      return venuesFromElements(elements, center, topics).filter(venue => venue.distanceKm <= 40);
    } catch (e) {
      return [];
    }
  }

  function placesEndpoint() {
    const host = root.location && root.location.hostname;
    if (!host) return '';
    if (host === 'localhost' || host === '127.0.0.1' || host === 'teachany.cn' || host === 'www.teachany.cn') {
      return `${root.location.origin}/api/pbl/places`;
    }
    return 'https://www.teachany.cn/api/pbl/places';
  }

  async function recallMapped(place, goal) {
    if (!place || !place.districtCode || !String(place.landmark || '').trim()) return { center: null, candidates: [] };
    const topics = searchTerms(goal, place);
    if (!topics.length) return { center: null, candidates: [] };
    const endpoint = placesEndpoint();
    if (endpoint) {
      try {
        const data = await fetchJson(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            place: {
              province: place.province, city: place.city, district: place.district, landmark: place.landmark,
            },
            topics,
          }),
        }, 15000);
        if (data && Array.isArray(data.candidates) && data.candidates.length) return data;
      } catch (e) { /* 接口未部署时改走直接检索 */ }
    }
    const center = await geocodeCenter(place);
    if (!center) return { center: null, candidates: [] };
    center.label = place.landmark;
    const candidates = await searchAround(center, topics);
    return { center, candidates };
  }

  function applyScores(bound, scores, goal, mode) {
    const byIndex = new Map((scores || []).map(row => [Number(row.index), row]));
    const rescored = (bound.candidates || []).map((venue, index) => {
      const row = byIndex.get(index);
      if (!row || row.noul == null) return venue;
      return { ...venue, noul: Number(row.noul), jevSource: 'jev' };
    });
    const next = bind(bound._place, goal, mode, rescored);
    if (!next) return null;
    next.placeLabel = bound.placeLabel;
    next.mode = mode;
    next.jevSource = next.status === 'fallback-unlisted' ? 'jev' : 'jev';
    next._place = bound._place;
    return next;
  }

  async function rescoreWithJev(bound, opts) {
    if (!bound || bound.status === 'fallback-unlisted' && !(bound.candidates || []).length) return bound;
    const endpoint = opts && opts.endpoint;
    const items = (bound.candidates || []).slice(0, 8);
    if (!endpoint || !items.length) return bound;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), (opts && opts.timeoutMs) || 8000);
    try {
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          stage: 'verify-places',
          goal: opts.goal || '',
          deliverable: opts.deliverable || '',
          placeLabel: bound.placeLabel || '',
          items: items.map((venue, index) => ({ index, name: venue.jevCandidate })),
        }),
        signal: controller.signal,
      });
      if (!resp.ok) return bound;
      const data = await resp.json();
      if (!data || data.fallback || !Array.isArray(data.scores)) return bound;
      return applyScores(bound, data.scores, opts.goal || '', bound.mode || 'pbl');
    } catch (e) {
      return bound;
    } finally {
      clearTimeout(timer);
    }
  }

  function findExperimentTask(tasks) {
    const list = tasks || [];
    const idx = list.findIndex(task => /动手|实验|制作|实施|探究/.test(String(task.stage || task.title || '')));
    if (idx >= 0) return idx;
    return list.length > 1 ? 1 : 0;
  }

  function applyToTasks(tasks, bound) {
    if (!bound || !tasks || !tasks.length) return tasks;
    const idx = findExperimentTask(tasks);
    const where = bound.distanceText
      ? `距${bound.originLabel || '学校'} ${bound.distanceText}·${bound.name}`
      : `${bound.placeLabel || ''}·${bound.ringLabel}·${bound.name}`;
    const note = `校外取证（${where}）：${bound.action}带回：${bound.evidence}。成人陪同，当日往返。`;
    return tasks.map((task, i) => {
      if (i !== idx) return task;
      const detail = String(task.detail || '').replace(/\n?校外取证（[\s\S]*$/,'');
      return { ...task, detail: `${detail}\n${note}`.trim(), offCampus: true };
    });
  }

  function applyToPathPlan(pathPlan, bound) {
    if (!pathPlan || !bound) return pathPlan;
    const phases = (pathPlan.phases || []).filter(phase => phase.id !== 'off-campus');
    phases.forEach(phase => {
      if (Array.isArray(phase._offCampusSteps)) {
        const drop = new Set(phase._offCampusSteps);
        phase.steps = (phase.steps || []).filter(step => !drop.has(step));
        delete phase._offCampusSteps;
      }
    });
    const note = bound.distanceText
      ? `${bound.name}，距${bound.originLabel || '学校'} ${bound.distanceText}。${bound.action}带回：${bound.evidence}`
      : `${bound.action}带回：${bound.evidence}`;
    const existing = phases.find(phase => /校外|实地|走访|参观|调查/.test(`${phase.phase || ''}${phase.venue || ''}`));
    if (existing) {
      existing.venue = '校外/实地';
      existing.venueKind = 'off-campus';
      existing.steps = [...(existing.steps || []), note];
      existing._offCampusSteps = [note];
    } else {
      const injected = {
        id: 'off-campus',
        phase: '校外实践',
        venue: '校外/实地',
        venueKind: 'off-campus',
        steps: [note, '成人陪同，当日往返'],
        acceptance: [bound.evidence, '成人陪同', '当日往返'],
        deliverable: bound.evidence,
        durationHint: bound.distanceText || bound.ringLabel,
      };
      const last = phases[phases.length - 1];
      if (last && /成果|展示|汇报|总结|反思/.test(last.phase || '')) phases.splice(phases.length - 1, 0, injected);
      else phases.push(injected);
    }
    phases.forEach((phase, i) => { phase.phaseIndex = i + 1; });
    pathPlan.phases = phases;
    pathPlan.offCampus = bound;
    return pathPlan;
  }

  function moduleHTML(opts) {
    const options = opts || {};
    const place = options.place || null;
    const bound = options.offCampus || null;
    const goal = options.goal || '';
    const terms = searchTerms(goal, place);
    const ready = !!(place && place.districtCode && String(place.landmark || '').trim());
    const where = ready
      ? [place.province, place.city && place.city !== place.province ? place.city : '', place.district, place.landmark].filter(Boolean).join('')
      : '';
    const objects = terms.length ? terms.join('、') : '这个课题没有需要到场看见的对象';
    let detail = '';
    if (!ready) {
      detail = '<p>填写区县，以及学校名称或地址。这里会列出周边具体地点、距离，并写成一次校外实践。</p>';
    } else if (options.status === 'searching') {
      detail = `<p>正在从「${esc(place.landmark)}」出发，检索${esc(objects)}。</p>`;
    } else if (!bound) {
      detail = `<p>已从「${esc(place.landmark)}」检索${esc(objects)}。服务半径内没有对得上的具体地点，这次不安排校外实践。</p>`;
    } else {
      detail = cardHTML(bound);
    }
    return `<div class="place-module">
      <p class="place-module-kicker">每周至少半天 · 纳入教育教学计划</p>
      <h3>周边资源分析与校外实践设计</h3>
      <p><b>分析对象：</b>${esc(objects)}</p>
      <p><b>出发地：</b>${where ? esc(where) : '未填写'}</p>
      ${detail}
    </div>`;
  }

  function cardHTML(bound) {
    if (!bound) return '';
    const dropped = (bound.dropped || []).slice(0, 4).map(venue => {
      const dist = venue.distanceText ? `，${venue.distanceText}` : '';
      return `${esc(venue.name)}（${esc(venue.ringLabel)}${esc(dist)}）`;
    }).join('、');
    const also = (bound.also || []).map(venue =>
      `${esc(venue.name)}，距${esc(bound.originLabel || '学校')} ${esc(venue.distanceText)}`
    ).join('；');
    const source = bound.jevSource === 'jev' ? 'Jev 筛选' : (bound.jevSource === 'map' ? '地图检索' : '本地筛选，Jev 未连上');
    const distLine = bound.distanceText
      ? `<p class="place-practice-dist">距${esc(bound.originLabel || '学校')} ${esc(bound.distanceText)}</p>`
      : '';
    return `<div class="place-practice">
      <p class="place-practice-kicker">校外实践 · ${esc(bound.ringLabel)} · ${esc(source)}</p>
      <p class="place-practice-name">${esc(bound.name)}</p>
      ${distLine}
      <p>${esc(bound.action)}</p>
      <p>带回：${esc(bound.evidence)}。成人陪同，当日往返。</p>
      ${also ? `<p class="place-practice-drop">附近还可看：${also}</p>` : ''}
      ${dropped ? `<p class="place-practice-drop">未采用：${dropped}</p>` : ''}
    </div>`;
  }

  function optionList(items, selected, placeholder) {
    const head = `<option value="">${esc(placeholder)}</option>`;
    return head + items.map(item =>
      `<option value="${esc(item.code)}"${item.code === selected ? ' selected' : ''}>${esc(item.name)}</option>`
    ).join('');
  }

  function byId(rootEl, id) {
    const sel = String(id || '').charAt(0) === '#' ? id : `#${id}`;
    return (rootEl || root.document).querySelector(sel);
  }

  function readPlace(rootEl, ids) {
    const q = sel => byId(rootEl, sel);
    const provinceCode = q(ids.province)?.value || '';
    const province = provinceOf(provinceCode);
    const cityCode = q(ids.city)?.value || '';
    let city = citiesOf(province).find(item => item.code === cityCode) || null;
    if (!city && province && isMunicipality(province)) city = citiesOf(province)[0];
    const districtCode = q(ids.district)?.value || '';
    const district = districtsOf(city).find(item => item.code === districtCode) || null;
    const landmark = q(ids.landmark)?.value?.trim() || '';
    if (!district) {
      return { provinceCode, province: province ? province.name : '', cityCode: city ? city.code : '', city: '', districtCode: '', district: '', landmark };
    }
    const cityName = city && city.name !== '市辖区' ? city.name : (province ? province.name : '');
    return {
      provinceCode,
      province: province ? province.name : '',
      cityCode: city ? city.code : '',
      city: cityName,
      districtCode: district.code,
      district: district.name,
      landmark,
    };
  }

  function syncSelects(rootEl, ids) {
    const q = sel => byId(rootEl, sel);
    const province = provinceOf(q(ids.province)?.value || '');
    const cityEl = q(ids.city);
    const districtEl = q(ids.district);
    if (!province) {
      cityEl.innerHTML = optionList([], '', '市');
      districtEl.innerHTML = optionList([], '', '区县');
      cityEl.hidden = true;
      districtEl.hidden = true;
      return;
    }
    const muni = isMunicipality(province);
    cityEl.hidden = muni;
    districtEl.hidden = false;
    if (muni) {
      const city = citiesOf(province)[0];
      cityEl.innerHTML = optionList([city], city.code, '市');
      cityEl.value = city.code;
      const prev = districtEl.value;
      districtEl.innerHTML = optionList(districtsOf(city), prev, '区县');
      return;
    }
    const prevCity = cityEl.value;
    cityEl.innerHTML = optionList(citiesOf(province), prevCity, '市');
    const city = citiesOf(province).find(item => item.code === cityEl.value) || null;
    const prevDistrict = districtEl.value;
    districtEl.innerHTML = optionList(districtsOf(city), prevDistrict, '区县');
    districtEl.hidden = !city;
  }

  function writePlace(rootEl, ids, place) {
    const q = sel => byId(rootEl, sel);
    if (!place) return;
    const provinceEl = q(ids.province);
    provinceEl.innerHTML = optionList(regions(), place.provinceCode || '', '不选');
    if (place.provinceCode) provinceEl.value = place.provinceCode;
    syncSelects(rootEl, ids);
    if (place.cityCode && q(ids.city)) q(ids.city).value = place.cityCode;
    syncSelects(rootEl, ids);
    if (place.districtCode && q(ids.district)) q(ids.district).value = place.districtCode;
    if (q(ids.landmark)) q(ids.landmark).value = place.landmark || '';
    const queryEl = q(ids.query || `${ids.district}-query`);
    if (queryEl && place.district) {
      const cityName = place.city && place.city !== place.province ? place.city : '';
      queryEl.value = [place.province, cityName, place.district].filter(Boolean).join(' ');
    }
  }

  function fieldIds(ids) {
    return {
      province: ids.province,
      city: ids.city,
      district: ids.district,
      landmark: ids.landmark,
      query: ids.query || `${ids.district}-query`,
    };
  }

  function renderSuggest(rootEl, ids, onChange) {
    const box = byId(rootEl, ids.query);
    const list = byId(rootEl, `${ids.query}-list`);
    if (!box || !list) return;
    const hits = searchDistricts(box.value);
    if (!hits.length) {
      list.hidden = true;
      list.innerHTML = '';
      return;
    }
    list.hidden = false;
    list.innerHTML = hits.map((row, index) =>
      `<button type="button" data-i="${index}">${esc(row.label)}</button>`
    ).join('');
    list.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', () => {
        const row = hits[Number(btn.getAttribute('data-i'))];
        writePlace(rootEl, ids, row);
        list.hidden = true;
        if (onChange) onChange(readPlace(rootEl, ids));
      });
    });
  }

  function mount(rootEl, ids, place, onChange) {
    ids = fieldIds(ids);
    const provinceEl = byId(rootEl, ids.province);
    if (!provinceEl) return;
    writePlace(rootEl, ids, place || {});
    const emit = () => { if (onChange) onChange(readPlace(rootEl, ids)); };
    [ids.province, ids.city, ids.district].forEach(sel => {
      byId(rootEl, sel)?.addEventListener('change', () => {
        if (sel === ids.province || sel === ids.city) syncSelects(rootEl, ids);
        const picked = readPlace(rootEl, ids);
        const queryEl = byId(rootEl, ids.query);
        if (queryEl && picked.district) {
          const cityName = picked.city && picked.city !== picked.province ? picked.city : '';
          queryEl.value = [picked.province, cityName, picked.district].filter(Boolean).join(' ');
        }
        emit();
      });
    });
    byId(rootEl, ids.landmark)?.addEventListener('input', emit);
    const queryEl = byId(rootEl, ids.query);
    queryEl?.addEventListener('input', () => renderSuggest(rootEl, ids, onChange));
    queryEl?.addEventListener('focus', () => renderSuggest(rootEl, ids, onChange));
  }

  function fieldsHTML(ids) {
    ids = fieldIds(ids);
    return `<div class="place-box">
      <span class="place-label">所在地（国内）</span>
      <div class="place-query-wrap">
        <input id="${esc(ids.query)}" class="place-landmark" type="text" placeholder="查询区县，如海淀、姑苏、南山" autocomplete="off" aria-label="查询区县" />
        <div id="${esc(ids.query)}-list" class="place-suggest" hidden></div>
      </div>
      <div class="place-row">
        <select id="${esc(ids.province)}" aria-label="省"></select>
        <select id="${esc(ids.city)}" aria-label="市"></select>
        <select id="${esc(ids.district)}" aria-label="区县"></select>
      </div>
      <input id="${esc(ids.landmark)}" class="place-landmark" type="text" placeholder="学校名称或地址，必填，用来计算距离" aria-label="学校名称或地址" />
      <p class="place-hint">区县用来圈定范围，学校名称或地址用来计算距离。召回写成具体地点和距离。附近没有可命名的合适地点时，不添加校外环节。</p>
    </div>`;
  }

  root.PlaceRings = {
    THRESHOLD,
    RINGS,
    RESEARCH_TYPES,
    derivePlaceSearch,
    searchTerms,
    searchDistricts,
    formatDistance,
    serviceRadiusKm,
    recallMapped,
    resolve,
    rescoreWithJev,
    applyToTasks,
    applyToPathPlan,
    cardHTML,
    moduleHTML,
    fieldsHTML,
    mount,
    readPlace,
    deriveIntents,
    localNoul,
  };
})(typeof globalThis !== 'undefined' ? globalThis : this);
