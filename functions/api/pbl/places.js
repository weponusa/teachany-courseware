/**
 * POST /api/pbl/places
 * Body: { place: { province, city, district, landmark }, topics: string[] }
 * 用学校名称或地址做圆心，按课题词召回具体地点，并计算距离。
 */

import { jsonResponse, CORS } from '../../_lib/llm-backends.js';

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

const RADII = [1000, 5000, 15000, 40000];

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
  if (km <= 1) return { id: 'r0', label: '校园周边' };
  if (km <= 5) return { id: 'r1', label: '街道' };
  if (km <= 15) return { id: 'r2', label: '区县' };
  if (km <= 40) return { id: 'r3', label: '城市当日' };
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
      data = await fetchJson(`https://photon.komoot.io/api/?limit=5&q=${encodeURIComponent(q)}`);
    } catch (e) {
      data = null;
    }
    const ranked = ((data && data.features) || []).map(feature => {
      const props = feature.properties || {};
      const coords = (feature.geometry && feature.geometry.coordinates) || [];
      const blob = `${props.name || ''}${props.city || ''}${props.state || ''}${props.district || ''}${props.county || ''}${props.street || ''}`;
      const stem = district.replace(/[区县市]$/, '');
      let score = 0;
      if (stem && blob.includes(stem)) score += 3;
      if (city && blob.includes(city.replace(/市$/, ''))) score += 2;
      const kind = String(place.landmark || '').match(/小学|中学|学校|幼儿园/);
      if (kind && props.name && String(props.name).includes(kind[0])) score += 4;
      if (kind && props.name && !String(props.name).includes(kind[0])) score -= 4;
      if (props.name && String(props.name).includes(String(place.landmark).slice(0, 4))) score += 2;
      return { lon: coords[0], lat: coords[1], name: props.name || place.landmark, score };
    }).filter(item => item.lat != null && item.lon != null && item.score > 0);
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
  return true;
}

function filtersFor(topics) {
  const blob = topics.join('');
  const filters = [];
  const names = topics.filter(term => /[\u4e00-\u9fa5]/.test(term) && term.length >= 2).slice(0, 4);
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

async function searchAround(center, topics) {
  const filters = filtersFor(topics);
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
      const wanted = topics.join('');
      const stems = [
        [/加氢|氢能|燃料电池/, /氢|燃料电池|加氢/],
        [/航空|航天|飞机|机场/, /航空|航天|飞机|机场/],
        [/回收|垃圾|填埋|转运|再生/, /回收|分类|填埋|转运|再生|垃圾|焚烧/],
        [/天文/, /天文/],
        [/自然博物馆|地质博物馆|化石|恐龙/, /自然|地质|化石|恐龙/],
        [/植物园/, /植物/],
        [/动物园/, /动物|昆虫|鸟/],
      ];
      const stem = stems.find(pair => pair[0].test(wanted));
      if (stem && !stem[1].test(placeName)) return;
      const lat = el.lat != null ? el.lat : (el.center && el.center.lat);
      const lon = el.lon != null ? el.lon : (el.center && el.center.lon);
      if (lat == null || lon == null) return;
      const distanceKm = haversineKm(center.lon, center.lat, lon, lat);
      if (distanceKm * 1000 > radius) return;
      const serviceLimitKm = serviceRadiusKm(tags.name, tags);
      if (serviceLimitKm != null && distanceKm > serviceLimitKm) return;
      const ring = ringFromKm(distanceKm);
      if (!ring) return;
      const street = tags['addr:street'] || '';
      const name = street && !String(tags.name).includes(street) ? `${tags.name}（${street}）` : tags.name;
      const prev = byName.get(name);
      if (prev && prev.distanceKm <= distanceKm) return;
      byName.set(name, {
        id: `map-${name}`,
        name,
        category: tags.waterway || tags.leisure || tags.tourism || tags.amenity || tags.historic || 'place',
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
        rank: (tags.waterway || tags.natural === 'water' || tags.leisure === 'park' || tags.tourism || tags.amenity || tags.historic) ? 2 : 1,
      });
    });
    let venues = [...byName.values()];
    if (venues.some(venue => venue.rank > 1)) venues = venues.filter(venue => venue.rank > 1);
    venues.sort((a, b) => a.distanceKm - b.distanceKm);
    if (radius <= 5000) {
      const strong = venues.filter(venue => venue.rank > 1);
      if (strong.length) return strong.slice(0, 8);
      if (!searchAround.weak) searchAround.weak = venues.slice(0, 8);
      continue;
    }
    if (venues.length) return venues.slice(0, 8);
  }
  return searchAround.weak || [];
}

export async function onRequestPost(context) {
  let body;
  try {
    body = await context.request.json();
  } catch (e) {
    return jsonResponse({ error: 'Invalid JSON' }, 400);
  }
  const place = body.place || {};
  const topics = (Array.isArray(body.topics) ? body.topics : []).map(item => String(item || '').trim()).filter(Boolean).slice(0, 6);
  const landmark = String(place.landmark || '').trim();
  if (!place.district || !landmark) return jsonResponse({ error: 'need district and school or address' }, 400);
  if (landmark.length > 80) return jsonResponse({ error: 'landmark too long' }, 400);
  const center = await geocodeCenter({ ...place, landmark });
  if (!center) return jsonResponse({ center: null, candidates: [], fallback: true, reason: 'geocode' });
  center.label = landmark;
  const candidates = await searchAround(center, topics);
  return jsonResponse({
    center: { lat: center.lat, lon: center.lon, name: center.name },
    candidates,
  });
}
