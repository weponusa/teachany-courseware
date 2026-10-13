/** @internal 校外实践统一数据契约、评分与路线降级逻辑。 */

export const ONE_HOUR_APPROX_RADIUS_KM = 30;

export const PLACE_TRAVEL_DEFAULTS = Object.freeze({
  mode: 'fixed-radius',
  limitMinutes: 60,
  radiusKm: ONE_HOUR_APPROX_RADIUS_KM,
  shape: 'parallelogram',
});

export const PLACE_TYPE_IDS = Object.freeze([
  'museum_named',
  'science_named',
  'park_named',
  'historic',
  'canal',
  'sluice',
  'wetland',
  'forest',
  'geology',
  'farm',
  'recycling',
  'wastewater',
  'energy',
  'industrial',
  'laboratory',
  'university',
  'community',
  'theatre',
  'marketplace',
  'fuel_named',
  'airport',
  'rail_transit',
  'hospital',
]);

const PLACE_TYPE_SET = new Set(PLACE_TYPE_IDS);

export function clampNumber(value, min, max, fallback) {
  const n = Number(value);
  return Number.isFinite(n) ? Math.min(max, Math.max(min, n)) : fallback;
}

export function normalizeTravelPolicy(raw = {}) {
  return {
    mode: PLACE_TRAVEL_DEFAULTS.mode,
    limitMinutes: PLACE_TRAVEL_DEFAULTS.limitMinutes,
    radiusKm: clampNumber(raw.radiusKm, 10, 50, PLACE_TRAVEL_DEFAULTS.radiusKm),
    shape: PLACE_TRAVEL_DEFAULTS.shape,
    label: '一小时近似范围',
  };
}

/** 经纬度包络矩形是平行四边形特例；东西/南北各取固定半径。 */
export function buildApproxBounds(center, radiusKm = ONE_HOUR_APPROX_RADIUS_KM) {
  const lat = Number(center?.lat);
  const lon = Number(center?.lon);
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) return null;
  const latPad = radiusKm / 111;
  const cos = Math.max(0.2, Math.cos(lat * Math.PI / 180));
  const lonPad = radiusKm / (111 * cos);
  return {
    minLat: lat - latPad,
    maxLat: lat + latPad,
    minLon: lon - lonPad,
    maxLon: lon + lonPad,
    radiusKm,
    shape: 'parallelogram',
  };
}

export function withinApproxBounds(center, candidate, radiusKm = ONE_HOUR_APPROX_RADIUS_KM) {
  const bounds = buildApproxBounds(center, radiusKm);
  const lat = Number(candidate?.lat);
  const lon = Number(candidate?.lon);
  if (!bounds || !Number.isFinite(lat) || !Number.isFinite(lon)) return false;
  return lat >= bounds.minLat && lat <= bounds.maxLat && lon >= bounds.minLon && lon <= bounds.maxLon;
}

function stringList(value, limit, maxLength = 24) {
  return [...new Set((Array.isArray(value) ? value : [])
    .map(item => String(item || '').trim())
    .filter(Boolean)
    .map(item => item.slice(0, maxLength)))].slice(0, limit);
}

export function normalizePlaceRequirement(raw = {}) {
  const queryGroups = (Array.isArray(raw.queryGroups) ? raw.queryGroups : [])
    .slice(0, 6)
    .map((group, index) => ({
      keywords: stringList(group?.keywords, 8),
      types: stringList(group?.types, 6).filter(type => PLACE_TYPE_SET.has(type)),
      priority: clampNumber(group?.priority, 1, 9, index + 1),
      purpose: String(group?.purpose || '').slice(0, 80),
    }))
    .filter(group => group.keywords.length || group.types.length);
  const queries = stringList(raw.queries, 10);
  const poi = stringList(raw.poi || raw.types, 8).filter(type => PLACE_TYPE_SET.has(type));
  if (!queryGroups.length && (queries.length || poi.length)) {
    queryGroups.push({ keywords: queries, types: poi, priority: 1, purpose: '' });
  }
  return {
    campusOnly: raw.campusOnly === true || raw.campus_only === true,
    object: String(raw.object || '').trim().slice(0, 120),
    see: stringList(Array.isArray(raw.see) ? raw.see : [raw.see], 8, 80),
    evidence: stringList(Array.isArray(raw.evidence) ? raw.evidence : [raw.evidence], 8, 80),
    activities: stringList(raw.activities, 8, 40),
    queryGroups,
    reject: stringList(raw.reject || raw.reject_names, 12, 30),
    accessNeeds: stringList(raw.accessNeeds, 8, 40),
    reason: String(raw.reason || '').trim().slice(0, 160),
  };
}

export function flattenPlaceQueries(requirement) {
  const req = normalizePlaceRequirement(requirement);
  const queries = [];
  const types = [];
  req.queryGroups
    .slice()
    .sort((a, b) => a.priority - b.priority)
    .forEach(group => {
      queries.push(...group.keywords);
      types.push(...group.types);
    });
  return {
    queries: [...new Set(queries)].slice(0, 10),
    types: [...new Set(types)].slice(0, 8),
  };
}

/** 兼容旧字段：仅为展示估算，不参与范围判定。 */
export function estimateDriveMinutes(distanceKm) {
  const km = Math.max(0, Number(distanceKm) || 0);
  return Math.max(5, Math.round(km / ONE_HOUR_APPROX_RADIUS_KM * 60));
}

export function travelTier(durationMinutes, travelPolicy = PLACE_TRAVEL_DEFAULTS) {
  const minutes = Number(durationMinutes);
  return Number.isFinite(minutes) && minutes <= normalizeTravelPolicy(travelPolicy).limitMinutes ? 'A' : 'C';
}

function accessStatusFor(candidate) {
  const explicit = String(candidate?.accessStatus || '');
  if (explicit) return explicit;
  const text = `${candidate?.name || ''} ${candidate?.category || ''}`;
  if (/实验室|研究院|研究所|工厂|车间|产业园|医院|机场|水厂|能源/.test(text)) {
    return 'appointment-required';
  }
  if (/博物馆|科技馆|纪念馆|公园|植物园|湿地|图书馆|展览馆/.test(text)) {
    return 'public-likely';
  }
  return 'unverified';
}

export function scorePlaceCandidate(candidate, context = {}) {
  const travel = normalizeTravelPolicy(context.travel || {});
  const distanceKm = Math.max(0, Number(candidate.distanceKm) || 0);
  const tier = distanceKm <= travel.radiusKm * Math.SQRT2 ? 'A' : 'C';
  const semantic = clampNumber(
    candidate.semanticScore ?? candidate.noul ?? (candidate.nameHit ? 0.8 : candidate.classHit ? 0.58 : 0.35),
    0,
    1,
    0.35,
  );
  const evidence = clampNumber(candidate.evidenceScore, 0, 1, candidate.nameHit ? 0.75 : 0.45);
  const operability = clampNumber(candidate.activityScore, 0, 1, candidate.canDo ? 0.68 : 0.35);
  const accessStatus = accessStatusFor(candidate);
  const access = accessStatus === 'verified-public' ? 1
    : accessStatus === 'public-likely' ? 0.7
      : accessStatus === 'appointment-required' ? 0.48 : 0.28;
  const travelScore = tier === 'A' ? Math.max(0.55, 1 - distanceKm / (travel.radiusKm * Math.SQRT2) * 0.45) : 0;
  const safety = /军事|保密|危化|矿井|生产线/.test(`${candidate.name || ''} ${candidate.category || ''}`)
    ? 0.15 : 0.78;
  const local = clampNumber(candidate.localUniqueness, 0, 1, 0.5);
  const total = Math.round((
    semantic * 25
    + evidence * 20
    + operability * 15
    + access * 15
    + travelScore * 10
    + safety * 10
    + local * 5
  ) * 10) / 10;
  return { total, tier, accessStatus, subscores: { semantic, evidence, operability, access, travel: travelScore, safety, local } };
}

export function rankPlaceCandidates(candidates, context = {}) {
  const travel = normalizeTravelPolicy(context.travel || {});
  const rows = (Array.isArray(candidates) ? candidates : []).map(candidate => {
    const scored = scorePlaceCandidate(candidate, { ...context, travel });
    return {
      ...candidate,
      tier: scored.tier,
      score: scored.total,
      accessStatus: scored.accessStatus,
      scoreBreakdown: scored.subscores,
    };
  });
  rows.sort((a, b) => {
    const tierOrder = { A: 0, C: 1 };
    return tierOrder[a.tier] - tierOrder[b.tier]
      || b.score - a.score
      || Number(a.distanceKm || 0) - Number(b.distanceKm || 0);
  });
  return rows;
}

export function dedupePlaceCandidates(candidates) {
  const byKey = new Map();
  (Array.isArray(candidates) ? candidates : []).forEach(candidate => {
    if (!candidate?.name) return;
    const coord = Number.isFinite(Number(candidate.lat)) && Number.isFinite(Number(candidate.lon))
      ? `${Number(candidate.lat).toFixed(4)},${Number(candidate.lon).toFixed(4)}`
      : '';
    const key = `${String(candidate.name).replace(/\s+/g, '')}|${coord}`;
    const old = byKey.get(key);
    if (!old || Number(candidate.rank || 0) > Number(old.rank || 0)) byKey.set(key, candidate);
  });
  return [...byKey.values()];
}
