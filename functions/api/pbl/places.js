/**
 * POST /api/pbl/places
 * Body: {
 *   place: { province, city, district, landmark, lat?, lon?, travelLimitMinutes? },
 *   goal: string,
 *   topics: string[],
 *   requirement?: PlaceRequirement,
 *   travel?: { mode, limitMinutes, preferredMinutes, departureTime }
 * }
 * 用学校实体做中心，按结构化实践需求宽召回，并以固定30公里经纬度包络平行四边形近似一小时范围。
 */

import { jsonResponse, CORS, callBackendLLM } from '../../_lib/llm-backends.js';
import {
  PLACE_TYPE_IDS,
  buildApproxBounds,
  dedupePlaceCandidates,
  flattenPlaceQueries,
  normalizePlaceRequirement,
  normalizeTravelPolicy,
  rankPlaceCandidates,
  withinApproxBounds,
} from '../../_lib/pbl-place-system.js';

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

const RADII = [45000];

function haversineKm(lon1, lat1, lon2, lat2) {
  const rad = Math.PI / 180;
  const dLat = (lat2 - lat1) * rad;
  const dLon = (lon2 - lon1) * rad;
  const a = Math.sin(dLat / 2) ** 2
    + Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLon / 2) ** 2;
  return 2 * 6371 * Math.asin(Math.min(1, Math.sqrt(a)));
}

function serviceRadiusKm(name, tags) {
  const text = `${name || ''} ${(tags && tags.amenity) || ''} ${(tags && tags.landuse) || ''} ${(tags && tags.tourism) || ''}`;
  if (/填埋|焚烧|landfill|waste_disposal|国家级|省级|全市|枢纽/.test(text)) return 40;
  if (/博物馆|科技馆|天文馆|大学|高校|景区|植物园|湿地公园|风景名胜/.test(text) && !/社区/.test(text)) return 40;
  if (/转运|中转|分拣中心|回收中心|处理中心|waste_transfer/.test(text)) return 15;
  if (/点|亭|驿站|社区|网格|投放|便民/.test(text)) return 2;
  if (/回收|分类|recycling|加油站|菜市|卫生服务/.test(text)) return 5;
  if (/公园|文化馆|图书馆|体育馆|展览馆/.test(text)) return 15;
  return null;
}

function ringFromKm(km) {
  if (km <= 43) return { id: 'r0', label: '一小时近似范围' };
  return null;
}

function formatDistance(km) {
  if (km == null || !isFinite(km)) return '';
  if (km < 1) return `${Math.max(50, Math.round(km * 1000 / 10) * 10)} m`;
  if (km < 10) return `${km.toFixed(1)} km`;
  return `${Math.round(km)} km`;
}

async function fetchJson(url, options, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs || 12000);
  try {
    const resp = await fetch(url, {
      ...(options || {}),
      headers: {
        Accept: 'application/json',
        'User-Agent': 'TeachAnyPlace/1.0',
        ...((options && options.headers) || {}),
      },
      signal: controller.signal,
    });
    if (!resp.ok) throw new Error(String(resp.status));
    return await resp.json();
  } finally {
    clearTimeout(timer);
  }
}

function amapKey(env) {
  return String(env?.AMAP_WEB_KEY || env?.AMAP_KEY || '').trim();
}

async function mapLimit(items, limit, worker) {
  const output = new Array(items.length);
  let cursor = 0;
  async function run() {
    while (cursor < items.length) {
      const index = cursor++;
      try {
        output[index] = await worker(items[index], index);
      } catch (error) {
        output[index] = { error: error.message };
      }
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, run));
  return output;
}

async function amapRequest(path, params, key, timeoutMs = 10000) {
  const search = new URLSearchParams({ ...params, key });
  const data = await fetchJson(`https://restapi.amap.com${path}?${search}`, null, timeoutMs);
  if (String(data?.status) !== '1') throw new Error(`AMap ${data?.infocode || data?.info || 'failed'}`);
  return data;
}

async function geocodeCenterAmap(place, env) {
  const key = amapKey(env);
  if (!key) return null;
  const address = [
    place.province,
    place.city && place.city !== place.province ? place.city : '',
    place.district,
    place.landmark,
  ].filter(Boolean).join('');
  if (!address) return null;
  const data = await amapRequest('/v3/geocode/geo', {
    address,
    city: String(place.city || '').replace(/市$/, ''),
    output: 'JSON',
  }, key);
  const rows = data.geocodes || [];
  const stem = schoolStem(place.landmark);
  const ranked = rows.map(row => {
    const [lon, lat] = String(row.location || '').split(',').map(Number);
    const blob = `${row.formatted_address || ''}${row.building?.name || ''}`;
    let score = 0;
    if (stem && blob.includes(stem)) score += 8;
    if (place.district && blob.includes(String(place.district).replace(/[区县市]$/, ''))) score += 2;
    return {
      lon,
      lat,
      name: row.formatted_address || place.landmark,
      score,
      source: 'amap',
      coordinateSystem: 'GCJ-02',
      confidence: score >= 8 ? 'high' : 'medium',
    };
  }).filter(row => Number.isFinite(row.lon) && Number.isFinite(row.lat) && (!stem || row.score >= 8));
  ranked.sort((a, b) => b.score - a.score);
  return ranked[0] || null;
}

async function searchAroundAmap(center, requirement, travel, env) {
  const key = amapKey(env);
  if (!key || center.source !== 'amap') return [];
  const { queries } = flattenPlaceQueries(requirement);
  const terms = queries.slice(0, 8);
  const batches = await mapLimit(terms, 3, async term => {
    const data = await amapRequest('/v3/place/around', {
      location: `${center.lon},${center.lat}`,
      keywords: term,
      radius: String(Math.ceil(travel.radiusKm * Math.SQRT2 * 1000)),
      offset: '20',
      page: '1',
      sortrule: 'weight',
      extensions: 'all',
      output: 'JSON',
    }, key, 12000);
    return (data.pois || []).map(poi => ({ poi, term }));
  });
  const rows = [];
  batches.forEach(batch => {
    if (!Array.isArray(batch)) return;
    batch.forEach(({ poi, term }) => {
      const [lon, lat] = String(poi.location || '').split(',').map(Number);
      if (!Number.isFinite(lon) || !Number.isFinite(lat)) return;
      const distanceKm = Number(poi.distance) / 1000 || haversineKm(center.lon, center.lat, lon, lat);
      const name = String(poi.name || '').trim();
      if (!name || !usable({ name }, queries)) return;
      rows.push({
        id: `amap-${poi.id || `${name}-${lon}-${lat}`}`,
        providerId: poi.id || '',
        provider: 'amap',
        name,
        address: Array.isArray(poi.address) ? poi.address.join('') : String(poi.address || ''),
        category: String(poi.type || '').split(';').slice(-1)[0] || 'place',
        categoryPath: String(poi.type || ''),
        phone: Array.isArray(poi.tel) ? poi.tel.join(' / ') : String(poi.tel || ''),
        queryHit: term,
        nameHit: name.includes(term),
        classHit: !name.includes(term),
        lon,
        lat,
        coordinateSystem: 'GCJ-02',
        distanceKm,
        rank: name.includes(term) ? 3 : 2,
        accessStatus: /博物馆|科技馆|公园|植物园|纪念馆/.test(name) ? 'public-likely' : 'unverified',
        canDo: `到「${name}」的开放区域核验课题对象并完成现场记录`,
        evidence: '地点、直线距离、现场对象与可复核记录',
        jevCandidate: `${name}（${poi.type || '地图地点'}，${formatDistance(distanceKm)}）：只根据名称和类别判断，不猜测未注明的展项`,
      });
    });
  });
  return dedupePlaceCandidates(rows);
}

async function attachTravelTimes(center, candidates, travel) {
  return candidates.slice(0, 20).map(candidate => ({
    ...candidate,
    rangeSource: 'fixed-radius',
    rangeShape: travel.shape,
    rangeRadiusKm: travel.radiusKm,
  }));
}

function bareLandmark(landmark) {
  let text = String(landmark || '').trim();
  text = text.replace(/^(北京市|北京|市辖区)/, '');
  text = text.replace(/^[\u4e00-\u9fa5]{1,8}(区|县)/, '');
  return text.trim() || String(landmark || '').trim();
}

function schoolStem(landmark) {
  return bareLandmark(landmark)
    .replace(/(附属|实验|第一|第二|第三|第四|第五)?(小学|中学|学校|幼儿园)/g, '')
    .replace(/[^\u4e00-\u9fa5]/g, '')
    .trim();
}

function expandPlaceTopics(topics) {
  const blob = (topics || []).join('');
  const extra = [];
  const rules = [
    [/水利|水能|水电|水闸|灌渠|运河|漕运|堤坝/, ['大运河', '运河', '水利', '水闸']],
    [/氢能|加氢|燃料电池/, ['加氢', '氢能']],
    [/光伏|太阳能/, ['光伏', '太阳能']],
    [/风电|风力发电/, ['风电']],
    [/农业|农场|温室|作物|种业|农庄|农园/, ['农场', '农业', '温室']],
    [/垃圾|回收|填埋|转运|再生/, ['回收', '垃圾', '转运']],
    [/天文|星空|行星|星象/, ['天文']],
    [/植物园|植物分类/, ['植物园']],
    [/湿地|候鸟|鸟类/, ['湿地']],
    [/化石|恐龙|地质/, ['地质', '自然']],
    [/文物|遗址|古迹|非遗|考古/, ['博物馆', '遗址']],
    [/航空|航天|飞机|机场|无人机/, ['航空', '航天', '航模', '机场']],
    [/机器人|人工智能|智能制造|工业互联网/, ['机器人', '智能', '产业园']],
    [/非遗|戏曲|手工艺/, ['非遗', '剧场']],
    [/食品|营养|乳品/, ['食品']],
    [/气象|地震|防灾/, ['气象', '地震']],
    [/海洋|港口|海事/, ['海洋', '港口']],
  ];
  rules.forEach(([re, words]) => { if (re.test(blob)) extra.push(...words); });
  (topics || []).forEach(term => {
    if (!term || term.length < 2 || term.length > 8) return;
    if (/智慧|测试|装置|利用|探究|设计|项目/.test(term)) return;
    extra.push(term);
  });
  return [...new Set(extra)].slice(0, 8);
}

async function geocodeCenter(place, env) {
  if (Number.isFinite(Number(place.lat)) && Number.isFinite(Number(place.lon))) {
    return {
      lat: Number(place.lat),
      lon: Number(place.lon),
      name: String(place.resolvedName || place.landmark || '出发地'),
      score: 10,
      source: String(place.coordinateSource || 'provided'),
      coordinateSystem: String(place.coordinateSystem || 'GCJ-02'),
      confidence: 'high',
    };
  }
  try {
    const amap = await geocodeCenterAmap(place, env);
    if (amap) return amap;
  } catch (e) { /* 高德未配置/失败则继续开放地图 */ }
  const bare = bareLandmark(place.landmark);
  const stem = schoolStem(place.landmark);
  const cityShort = String(place.city || '').replace(/市$/, '');
  const queries = [bare, place.landmark, `${cityShort}${bare}`];
  for (const q of queries) {
    if (!q) continue;
    let data = null;
    try {
      data = await fetchJson(`https://photon.komoot.io/api/?limit=5&q=${encodeURIComponent(q)}`);
    } catch (e) {
      data = null;
    }
    const ranked = ((data && data.features) || []).map(feature => {
      const props = feature.properties || {};
      const coords = (feature.geometry && feature.geometry.coordinates) || [];
      const name = String(props.name || '');
      let score = 0;
      if (stem.length >= 2 && name.includes(stem)) score += 8;
      else if (stem.length >= 2) score -= 8;
      const kind = String(place.landmark || '').match(/小学|中学|学校|幼儿园/);
      if (kind && name.includes(kind[0])) score += 2;
      return {
        lon: coords[0],
        lat: coords[1],
        name: name || place.landmark,
        score,
        source: 'photon',
        coordinateSystem: 'WGS84',
        confidence: score >= 8 ? 'high' : 'medium',
      };
    }).filter(item => item.lat != null && item.lon != null && item.score > 0 && (stem.length < 2 || String(item.name).includes(stem)));
    ranked.sort((a, b) => b.score - a.score);
    if (ranked[0]) return ranked[0];
  }
  return null;
}

function usable(tags, topics) {
  if (!tags || !tags.name || String(tags.name).length < 2) return false;
  const blob = topics.join('');
  if (tags.highway && !/路|街|交通|站/.test(blob)) return false;
  if (tags.place && /city|town|village|hamlet|suburb/.test(tags.place) && !/村|镇/.test(blob)) return false;
  if (tags.landuse === 'residential' || tags.landuse === 'construction') return false;
  const placeName = String(tags.name || '');
  if (/社区|家园|小区|公寓|宿舍|住宅/.test(placeName) && !/公园|博物馆|水闸|农场|湿地/.test(placeName)) return false;
  if (/(路|街|街道)$/.test(placeName) && !/公园|博物馆|水闸/.test(placeName)) return false;
  if (/店$|超市|饭店|餐厅|便民|管理处|服务处|办事处|综合楼|办公楼/.test(placeName) && !/市场|商场/.test(blob)) return false;
  if (/市场/.test(placeName) && !/市场|商业|物价|买卖/.test(blob)) return false;
  return true;
}

function filtersFor(topics, poi) {
  const expanded = expandPlaceTopics(topics);
  const blob = expanded.join('');
  const classes = new Set(poi || []);
  const filters = [];
  if (expanded.length) filters.push({ name: expanded.slice(0, 8).join('|') });
  if (/公园|景区|绿地/.test(blob)) filters.push({ park: true });
  if (/博物馆|科技馆|天文馆|展览/.test(blob)) filters.push({ museum: true });
  if (/加油站/.test(blob)) filters.push({ fuel: true });
  if (/工厂|产业园|车间/.test(blob) || classes.has('industrial')) filters.push({ industrial: true });
  if (/实验室|大学|高校/.test(blob)) filters.push({ university: true });
  if (/村落|古建|斗拱|文保|遗址|古迹/.test(blob)) filters.push({ historic: true });
  if (/农田|作物|农场|温室|农业/.test(blob) || classes.has('farm')) filters.push({ farm: true });
  if (/垃圾|回收|填埋|再生|转运/.test(blob) || classes.has('recycling')) filters.push({ waste: true });
  if (/水利|水能|运河|水闸|灌渠|漕运/.test(blob) || classes.has('canal')) filters.push({ canal: true });
  if (/水闸|船闸|堤坝/.test(blob) || classes.has('sluice')) filters.push({ sluice: true });
  if (classes.has('wastewater') || /污水|水厂/.test(blob)) filters.push({ wastewater: true });
  if (classes.has('community') || /社区/.test(blob)) filters.push({ community: true });
  if (classes.has('theatre') || /剧场|戏院|戏曲/.test(blob)) filters.push({ theatre: true });
  if (classes.has('marketplace') || /市场|菜市/.test(blob)) filters.push({ marketplace: true });
  if (classes.has('wetland')) filters.push({ wetland: true });
  if (classes.has('forest')) filters.push({ forest: true });
  if (classes.has('geology')) filters.push({ geology: true });
  if (classes.has('energy')) filters.push({ energy: true });
  if (classes.has('laboratory')) filters.push({ laboratory: true });
  if (classes.has('university')) filters.push({ university: true });
  if (classes.has('hospital')) filters.push({ hospital: true });
  if (classes.has('airport')) filters.push({ airport: true });
  if (classes.has('rail_transit')) filters.push({ railTransit: true });
  if ((classes.has('museum_named') || classes.has('park_named') || classes.has('fuel_named')) && expanded.length) {
    filters.push({ namedClass: expanded.slice(0, 4).join('|'), museumNamed: classes.has('museum_named'), parkNamed: classes.has('park_named'), fuelNamed: classes.has('fuel_named') });
  }
  // 宽召回只取少量地图类别候选，之后必须经过 Jev；不是直接推荐。
  if (classes.has('museum_named') || classes.has('science_named')) filters.push({ museumBroad: true });
  if (classes.has('park_named')) filters.push({ parkBroad: true });
  if (classes.has('fuel_named')) filters.push({ fuelBroad: true });
  return filters;
}

async function searchAround(center, topics, poi) {
  const filters = filtersFor(topics, poi);
  searchAround.weak = null;
  for (const radius of RADII) {
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
      if (filter.canal) lines.push(`nwr(${around})["waterway"~"canal|river"]["name"];`);
      if (filter.sluice) {
        lines.push(`nwr(${around})["man_made"~"sluice_gate|weir"]["name"];`);
        lines.push(`nwr(${around})["waterway"="lock_gate"]["name"];`);
      }
      if (filter.wastewater) lines.push(`nwr(${around})["man_made"="wastewater_plant"]["name"];`);
      if (filter.community) lines.push(`nwr(${around})["amenity"="community_centre"]["name"];`);
      if (filter.theatre) lines.push(`nwr(${around})["amenity"="theatre"]["name"];`);
      if (filter.marketplace) lines.push(`nwr(${around})["amenity"="marketplace"]["name"];`);
      if (filter.wetland) lines.push(`nwr(${around})["natural"="wetland"]["name"];`);
      if (filter.forest) {
        lines.push(`nwr(${around})["landuse"="forest"]["name"];`);
        lines.push(`nwr(${around})["natural"="wood"]["name"];`);
      }
      if (filter.geology) lines.push(`nwr(${around})["geological"]["name"];`);
      if (filter.energy) lines.push(`nwr(${around})["power"~"plant|generator"]["name"];`);
      if (filter.laboratory) lines.push(`nwr(${around})["amenity"="research_institute"]["name"];`);
      if (filter.hospital) lines.push(`nwr(${around})["amenity"="hospital"]["name"];`);
      if (filter.airport) lines.push(`nwr(${around})["aeroway"="aerodrome"]["name"];`);
      if (filter.railTransit) lines.push(`nwr(${around})["railway"~"station|halt"]["name"];`);
      if (filter.namedClass && filter.museumNamed) lines.push(`nwr(${around})["tourism"="museum"]["name"~"${filter.namedClass}"];`);
      if (filter.namedClass && filter.parkNamed) lines.push(`nwr(${around})["leisure"="park"]["name"~"${filter.namedClass}"];`);
      if (filter.namedClass && filter.fuelNamed) lines.push(`nwr(${around})["amenity"="fuel"]["name"~"${filter.namedClass}"];`);
      if (filter.museumBroad) lines.push(`nwr(${around})["tourism"="museum"]["name"];`);
      if (filter.parkBroad) lines.push(`nwr(${around})["leisure"="park"]["name"];`);
      if (filter.fuelBroad) lines.push(`nwr(${around})["amenity"="fuel"]["name"];`);
    });
    if (!lines.length) return [];
    let elements = [];
    try {
      const query = `[out:json][timeout:12];(${lines.join('')});out center 12;`;
      const data = await fetchJson('https://lz4.overpass-api.de/api/interpreter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
        body: `data=${encodeURIComponent(query)}`,
      }, 14000);
      elements = (data && data.elements) || [];
    } catch (e) {
      elements = [];
    }
    const byName = new Map();
    elements.forEach(el => {
      const tags = el.tags || {};
      if (!usable(tags, topics)) return;
      const placeName = String(tags.name || '');
      if (/小学|中学|幼儿园/.test(placeName)) return;
      const wanted = expandPlaceTopics(topics).join('');
      const stems = [
        [/水利|水能|水电|运河|水闸|灌渠|漕运/, /运河|水利|水闸|灌渠|漕运|堤坝/],
        [/加氢|氢能|燃料电池/, /氢|燃料电池|加氢/],
        [/航空|航天|飞机|机场/, /航空|航天|飞机|机场/],
        [/回收|垃圾|填埋|转运|再生/, /回收|分类|填埋|转运|再生|垃圾|焚烧/],
        [/天文/, /天文/],
        [/自然博物馆|地质博物馆|化石|恐龙/, /自然|地质|化石|恐龙/],
        [/植物园/, /植物/],
        [/动物园/, /动物|昆虫|鸟/],
        [/农业|农场|农庄|种业|温室/, /农业|农场|农庄|农园|种业|温室|果园/],
      ];
      const classes = new Set(poi || []);
      const classHit = !!(tags.waterway || tags.amenity === 'recycling' || tags.amenity === 'waste_transfer_station'
        || tags.man_made === 'wastewater_plant' || /sluice_gate|weir/.test(tags.man_made || '')
        || (classes.has('museum_named') && tags.tourism === 'museum')
        || (classes.has('science_named') && tags.tourism === 'museum')
        || (classes.has('park_named') && tags.leisure === 'park')
        || (classes.has('fuel_named') && tags.amenity === 'fuel')
        || (classes.has('farm') && /farmland|greenhouse_horticulture/.test(tags.landuse || ''))
        || (classes.has('industrial') && tags.landuse === 'industrial')
        || (classes.has('community') && tags.amenity === 'community_centre')
        || (classes.has('theatre') && tags.amenity === 'theatre')
        || (classes.has('marketplace') && tags.amenity === 'marketplace'));
      const extendedClassHit = classHit
        || (classes.has('wetland') && tags.natural === 'wetland')
        || (classes.has('forest') && /forest|wood/.test(`${tags.landuse || ''}${tags.natural || ''}`))
        || (classes.has('geology') && !!tags.geological)
        || (classes.has('energy') && /plant|generator/.test(tags.power || ''))
        || (classes.has('laboratory') && tags.amenity === 'research_institute')
        || (classes.has('university') && tags.amenity === 'university')
        || (classes.has('hospital') && tags.amenity === 'hospital')
        || (classes.has('airport') && tags.aeroway === 'aerodrome')
        || (classes.has('rail_transit') && /station|halt/.test(tags.railway || ''));
      const stem = stems.find(pair => pair[0].test(wanted));
      if (stem && !stem[1].test(placeName) && !extendedClassHit) return;
      const lat = el.lat != null ? el.lat : (el.center && el.center.lat);
      const lon = el.lon != null ? el.lon : (el.center && el.center.lon);
      if (lat == null || lon == null) return;
      const distanceKm = haversineKm(center.lon, center.lat, lon, lat);
      if (distanceKm * 1000 > radius) return;
      const ring = ringFromKm(distanceKm);
      if (!ring) return;
      const street = tags['addr:street'] || '';
      const name = street && !String(tags.name).includes(street) ? `${tags.name}（${street}）` : tags.name;
      const prev = byName.get(name);
      if (prev && prev.distanceKm <= distanceKm) return;
      byName.set(name, {
        id: `map-${name}`,
        name,
        category: tags.waterway || tags.leisure || tags.tourism || tags.amenity || tags.historic || tags.landuse || tags.man_made || 'place',
        classHit: extendedClassHit || undefined,
        ringId: ring.id,
        ringLabel: ring.label,
        distanceKm,
        noul: 0.74,
        jevSource: 'map',
        canDo: /填埋|焚烧/.test(name)
          ? `在「${name}」的开放参观或外围观察垃圾最终去向，不进入填埋作业面`
          : /回收|分类|转运|再生|垃圾/.test(name)
            ? `在「${name}」的对外开放区域记录垃圾怎样被分类、回收或运走，不进入作业区`
            : `到「${name}」完成和课题对应的现场记录，只停留在对外开放区域`,
        evidence: '地点名称、距离学校的记录、现场看到的现象',
        jevCandidate: [
          name,
          `距${center.label || '学校'} ${formatDistance(distanceKm)}`,
          '在开放区域要看见的对象必须就是课题本身，不能只是地名里有相同的字',
        ].join('。'),
        lat,
        lon,
        rank: expandPlaceTopics(topics).some(term => String(tags.name || '').includes(term))
          ? 3
          : (extendedClassHit || tags.natural === 'water' || tags.historic ? 2 : 1),
      });
    });
    let venues = [...byName.values()];
    if (venues.some(venue => venue.rank > 1)) venues = venues.filter(venue => venue.rank > 1);
    venues.sort((a, b) => b.rank - a.rank || a.distanceKm - b.distanceKm);
    if (radius <= 5000) {
      const strong = venues.filter(venue => venue.rank > 1);
      if (strong.length) return strong.slice(0, 8);
      if (!searchAround.weak) searchAround.weak = venues.slice(0, 8);
      continue;
    }
    if (venues.length) return venues.slice(0, 8);
  }
  const photonVenues = await venuesFromPhoton(center, topics, searchAround.city || '');
  const merged = [...(searchAround.weak || []), ...photonVenues];
  const seen = new Set();
  return merged.filter(venue => {
    if (!venue || !venue.name || seen.has(venue.name)) return false;
    seen.add(venue.name);
    return true;
  }).sort((a, b) => a.distanceKm - b.distanceKm).slice(0, 8);
}

async function venuesFromPhoton(center, topics, city) {
  const queries = expandPlaceTopics(topics).slice(0, 4);
  const cityShort = String(city || '').replace(/市$/, '');
  const terms = [...new Set([
    ...queries,
    ...queries.slice(0, 2).map(term => (cityShort ? `${cityShort}${term}` : '')),
  ])].filter(Boolean).slice(0, 6);
  const lists = await Promise.all(terms.map(async term => {
    try {
      return await fetchJson(`https://photon.komoot.io/api/?limit=6&lat=${center.lat}&lon=${center.lon}&location_bias_scale=0.2&q=${encodeURIComponent(term)}`);
    } catch (e) {
      return null;
    }
  }));
  const venues = [];
  lists.forEach(data => {
    ((data && data.features) || []).forEach(feature => {
      const props = feature.properties || {};
      const coords = (feature.geometry && feature.geometry.coordinates) || [];
      const tags = { name: props.name || '' };
      if (props.osm_key && props.osm_value) tags[props.osm_key] = props.osm_value;
      if (!usable(tags, topics)) return;
      if (/小学|中学|幼儿园/.test(tags.name)) return;
      const distanceKm = haversineKm(center.lon, center.lat, coords[0], coords[1]);
      if (!isFinite(distanceKm) || distanceKm > 43) return;
      const ring = ringFromKm(distanceKm);
      if (!ring) return;
      venues.push({
        id: `map-${tags.name}`,
        name: tags.name,
        category: tags.waterway || tags.tourism || tags.leisure || 'place',
        classHit: !!tags.waterway || undefined,
        ringId: ring.id,
        ringLabel: ring.label,
        distanceKm,
        noul: 0.74,
        jevSource: 'map',
        canDo: `到「${tags.name}」的开放区域完成和课题对应的现场记录`,
        evidence: '地点名称、距离学校的记录、现场看到的现象',
        jevCandidate: `${tags.name}。距出发点 ${formatDistance(distanceKm)}。只在开放区域观察。`,
        lat: coords[1],
        lon: coords[0],
        rank: 2,
      });
    });
  });
  return venues;
}

const PLACE_PLAN_PROMPT = `你是 PBL 校外实践的检索规划员。你不调用地图，也不编造任何地点。程序会先把出发地定位成圆心（区划与机构冲突时以机构坐标为准），再按你给的检索词和类别，在圆心周围向开放地图检索。提示词里不写学校名字。

地图实际收到的参数是：
- 中心：出发地坐标
- 范围：东西、南北各约30公里的经纬度包络平行四边形，统一作为“一小时近似范围”，不再划圈层
- 路 A：queryGroups.keywords 做名称检索
- 路 B：queryGroups.types 做地图类别宽召回。类别本身就是对象时，名称不必等于课题原文
你只输出最可能写进地名的词。词要覆盖「主题专属词 × 场所类型」，不要输出整句口号，也不要一次堆出几十个同义词。

规划步骤：
1. 从项目目标抽出能看见、能调查、能访谈或能搜集数据的对象。丢掉学段、学科、产出、报告、测试、智慧、未来、科学、生态、生活这些修饰。装置、模型、小程序、文章的对象是它模仿的现实事物。
2. 先判断校外是否必要：项目能在校园、家庭、课堂或屏幕内完成，且题目没有明确要求外部调查、参观、访谈或现实样本时，campus_only 为 true，queries 和 poi 为空。制作水火箭、纸桥、乐器、红绿灯原型等课堂工程，不要仅因为普通科技馆“可能有展项”就安排出行；设计营养午餐且数据来自学生、家庭或校内食堂，也留在校园。纯数学、编程、数据分析、阅读写作、课件、课程答辩默认留校。题目明确写“校园观察、校园调查、家庭调查”时，不得擅自改成校外。主题过于空泛（如只说设计周末营或研学路线）且没有可观察对象时，也不得自行编造地点类型。
3. 用主题词交叉这些场所，但只把交叉结果里真会出现在店名里的字放进 queries：科普场馆、专题博物馆、高校里对公众开放的实验或实训、产业园展厅、示范基地、社区与非遗、自然与田野。小学偏科普馆和体验馆；高中可加实验室、实训基地、企业展厅。
4. 上下游只取学生到得了现场的环节：原料、研发展示、生产参观、检测、应用、废弃与循环。军事、保密、未开放的生产一线不要检索，改搜其科普馆或展厅。
5. 通用类型只是宽召回入口，不是相关性证据。普通博物馆、科技馆、剧场、图书馆、农场不能因为类型相近就断言有某个展项；候选名称未明确对象时，留给后续审核，不要在 see/evidence 中编造展览内容。
6. 纯餐饮、普通商场、食堂、已关闭场所、小区、道路、学校本身不作为校外实践点。只有课题明确研究市场交易、社区行为或餐饮供应链，并且候选名称能确认对应现场时例外。
7. 排序由程序按距离做。你用 queries 的先后表达优先级：主题匹配最高，其次是能观察或动手的场所。

types 最多 8 个，只能从这些编号里选：
museum_named 博物馆；science_named 科技馆；park_named 公园；historic 遗址纪念馆；canal 河流运河；sluice 水闸；wetland 湿地；forest 森林；geology 地质；farm 农田温室；recycling 回收转运；wastewater 污水处理；energy 能源设施；industrial 产业园工厂展厅；laboratory 实验室研究院；university 高校；community 社区服务；theatre 剧场；marketplace 市场；fuel_named 充换电或加氢；airport 机场；rail_transit 轨道交通；hospital 医院健康科普。
不要用「全部博物馆」「全部公园」「全部大学」。

只输出 JSON：
{"campusOnly":false,"object":"","see":[],"evidence":[],"activities":[],"queryGroups":[{"keywords":[],"types":[],"priority":1,"purpose":""}],"reject":[],"accessNeeds":[],"reason":""}

例子（不写学校）：
1. 航空航天。queries: ["航空","航天","航模","机场","科技馆"]。poi: ["museum_named"]。留下航空馆、科技馆相关展区、航模场地、开放的机场观光。不搜封闭机务区，不搜「模型」。
2. 现代农业。queries: ["温室","农场","农业","植物工厂","批发市场"]。poi: ["farm","marketplace"]。留下示范园、试验田、产地市场。纯采摘乐园若看不出课程目标，不放进 queries。
3. 乡村振兴。queries: ["村史","非遗","合作社","农耕"]。poi: ["historic","community"]。留下村史馆、工坊、合作社。不把餐饮店当实践点。
4. 水利或水能。queries: ["运河","水利","水闸","灌渠"]。poi: ["canal","sluice","museum_named"]。水体类别即使名字里没有口号也保留。带这些字的小区和道路丢掉。
5. 人工智能或机器人。queries: ["机器人","科技馆","创客"]。poi: ["museum_named"]。不因为带「智能」就搜所有园区。
6. 垃圾或环保。queries: ["回收","垃圾","转运","污水"]。poi: ["recycling","wastewater"]。
7. 交换校服的小程序、写作、口算。campus_only: true。queries: []。poi: []。
8. 制作水火箭、纸桥、乐器或红绿灯原型，题目没有要求外部调查。campus_only: true。不要为了普通科技馆强加出行。
9. 设计一周营养午餐，调查对象是本校学生、家庭或校内食堂。campus_only: true。只有题目明确研究中央厨房、食品检测或校外供应链时才检索对应地点。
10. 初等函数、微积分、编程可视化、公开数据分析、课堂答辩。campus_only: true。
11. 校园夜观、校园气象站、校园屋顶光伏、家庭用水调查。campus_only: true；不要把“校园/家庭”改成公园或场馆。
12. 只写“设计两天周末营”而没有主题对象。campus_only: true；信息不足，不编农场、社区或科普馆。`;

function cleanQueries(list) {
  return [...new Set((list || []).map(item => String(item || '').trim()).filter(item => (
    /^[\u4e00-\u9fa5]{2,8}$/.test(item) && !/^(智慧|测试|未来|科学|生态|能源|生活|项目|装置|博物馆|公园|大学|商场)$/.test(item)
  )))].slice(0, 8);
}

const POI_IDS = new Set(PLACE_TYPE_IDS);

function cleanPoi(list) {
  return [...new Set((list || []).map(item => String(item || '').trim()).filter(item => POI_IDS.has(item)))].slice(0, 4);
}

async function planPlaceQueries(env, topics, goal) {
  const fallback = expandPlaceTopics(topics);
  const objective = String(goal || '').trim() || topics.join('、');
  try {
    const { content } = await callBackendLLM(env, [
      { role: 'system', content: PLACE_PLAN_PROMPT },
      { role: 'user', content: `项目目标：${objective}\n已抽出的词：${topics.join('、')}` },
    ], { maxTokens: 500, temperature: 0, timeoutMs: 8000 });
    const matched = String(content || '').match(/\{[\s\S]*\}/);
    const plan = JSON.parse(matched ? matched[0] : '');
    const requirement = normalizePlaceRequirement(plan);
    if (requirement.campusOnly) return { campus: true, queries: [], poi: [], requirement };
    let { queries, types: poi } = flattenPlaceQueries(requirement);
    queries = cleanQueries(queries.length ? queries : plan.queries);
    poi = cleanPoi(poi.length ? poi : plan.poi);
    const normalized = normalizePlaceRequirement({
      ...requirement,
      queries: queries.length ? queries : fallback,
      poi,
    });
    if (queries.length || poi.length) {
      return {
        campus: false,
        queries: queries.length ? queries : fallback,
        poi,
        requirement: normalized,
      };
    }
  } catch (e) { /* 规划失败就用词表 */ }
  const requirement = normalizePlaceRequirement({
    object: goal,
    queries: fallback,
    poi: [],
    reason: 'planner-fallback',
  });
  return { campus: false, queries: fallback, poi: [], requirement };
}

function rankPlaces(candidates) {
  return (candidates || []).map(venue => {
    const km = venue.distanceKm;
    const tier = km == null || km <= 15 ? 'A' : (km <= 30 ? 'B' : 'C');
    const name = String(venue.name || '');
    return {
      ...venue,
      tier,
      activity: venue.canDo,
      risk: /填埋|焚烧|污水|工厂|车间|水厂/.test(name)
        ? '只停留在开放参观区，不进入作业面。成人陪同，提前确认是否接待团队。'
        : '成人陪同。只进入对公众或团队开放的区域，出发前核实预约和开放时间。',
      minutes: km == null ? null : Math.max(20, Math.round(km * 4 + 15)),
    };
  }).sort((a, b) => {
    const order = { A: 0, B: 1, C: 2 };
    if (order[a.tier] !== order[b.tier]) return order[a.tier] - order[b.tier];
    return (a.distanceKm || 99) - (b.distanceKm || 99);
  }).slice(0, 5);
}

export async function onRequestPost(context) {
  let body;
  try {
    body = await context.request.json();
  } catch (e) {
    return jsonResponse({ error: 'Invalid JSON' }, 400);
  }
  const place = body.place || {};
  const topics = (Array.isArray(body.topics) ? body.topics : []).map(item => String(item || '').trim()).filter(Boolean).slice(0, 8);
  const goal = String(body.goal || '').trim().slice(0, 800);
  const landmark = String(place.landmark || '').trim();
  if (!landmark && !(Number.isFinite(Number(place.lat)) && Number.isFinite(Number(place.lon)))) {
    return jsonResponse({ error: 'need school/address or coordinates' }, 400);
  }
  if (landmark.length > 80) return jsonResponse({ error: 'landmark too long' }, 400);
  const travel = normalizeTravelPolicy(body.travel || place.travel || place);
  const center = await geocodeCenter({ ...place, landmark }, context.env);
  if (!center) return jsonResponse({ center: null, candidates: [], fallback: true, reason: 'geocode' });
  center.label = landmark;
  searchAround.city = place.city || '';
  let plan;
  if (body.requirement && typeof body.requirement === 'object') {
    const requirement = normalizePlaceRequirement(body.requirement);
    const flattened = flattenPlaceQueries(requirement);
    plan = {
      campus: requirement.campusOnly,
      queries: cleanQueries(flattened.queries),
      poi: cleanPoi(flattened.types),
      requirement,
    };
  } else {
    plan = await planPlaceQueries(context.env, topics, goal);
  }
  if (plan.campus) {
    return jsonResponse({
      center: {
        lat: center.lat,
        lon: center.lon,
        name: center.name,
        source: center.source,
        coordinateSystem: center.coordinateSystem,
        confidence: center.confidence,
      },
      candidates: [],
      queries: [],
      requirement: plan.requirement,
      travel,
      reason: 'campus',
    });
  }
  let candidates = [];
  const warnings = [];
  try {
    candidates = await searchAroundAmap(center, plan.requirement, travel, context.env);
  } catch (e) {
    warnings.push(`高德地点检索失败：${e.message}`);
  }
  if (!candidates.length) {
    candidates = await searchAround(center, plan.queries.length ? plan.queries : topics, plan.poi);
    warnings.push('使用开放地图召回；范围按固定30公里经纬度包络近似');
  }
  const inRange = dedupePlaceCandidates(candidates)
    .filter(candidate => withinApproxBounds(center, candidate, travel.radiusKm));
  const withTravel = await attachTravelTimes(center, inRange, travel);
  const ranked = rankPlaceCandidates(withTravel, { travel })
    .filter(candidate => candidate.tier !== 'C')
    .slice(0, 12);
  warnings.push('“一小时”按学校周边东西/南北各约30公里的平行四边形近似，不代表实时路况');
  const area = buildApproxBounds(center, travel.radiusKm);
  return jsonResponse({
    center: {
      lat: center.lat,
      lon: center.lon,
      name: center.name,
      source: center.source,
      coordinateSystem: center.coordinateSystem,
      confidence: center.confidence,
    },
    candidates: ranked,
    ranked,
    route: ranked.slice(0, 3),
    queries: plan.queries,
    poi: plan.poi || [],
    requirement: plan.requirement,
    travel,
    area,
    warnings,
    routeSource: 'fixed-radius',
  });
}
