import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {
  buildApproxBounds,
  estimateDriveMinutes,
  flattenPlaceQueries,
  normalizePlaceRequirement,
  normalizeTravelPolicy,
  rankPlaceCandidates,
  travelTier,
  withinApproxBounds,
} from '../functions/_lib/pbl-place-system.js';
import { onRequestPost as placesPost } from '../functions/api/pbl/places.js';

const travel = normalizeTravelPolicy({
  transportMode: 'driving',
  travelLimitMinutes: 60,
});
assert.equal(travel.mode, 'fixed-radius');
assert.equal(travel.limitMinutes, 60);
assert.equal(travel.radiusKm, 30);
assert.equal(travel.shape, 'parallelogram');
assert.equal(travelTier(20, travel), 'A');
assert.equal(travelTier(61, travel), 'C');
assert.equal(estimateDriveMinutes(10), 20);
const bounds = buildApproxBounds({ lat: 22.55, lon: 114.05 }, 30);
assert.ok(bounds.maxLat > 22.8 && bounds.minLat < 22.3);
assert.equal(withinApproxBounds({ lat: 22.55, lon: 114.05 }, { lat: 22.6, lon: 114.1 }, 30), true);
assert.equal(withinApproxBounds({ lat: 22.55, lon: 114.05 }, { lat: 23.1, lon: 114.1 }, 30), false);

const requirement = normalizePlaceRequirement({
  campusOnly: false,
  object: '现代农业',
  see: ['温室', '智能灌溉'],
  evidence: ['灌溉记录'],
  activities: ['观察', '访谈'],
  queryGroups: [
    { keywords: ['温室', '农场'], types: ['farm', 'museum_named', 'bad-type'], priority: 1 },
  ],
  reject: ['住宅'],
});
assert.deepEqual(flattenPlaceQueries(requirement), {
  queries: ['温室', '农场'],
  types: ['farm', 'museum_named'],
});

const ranked = rankPlaceCandidates([
  {
    name: '现代农业示范园',
    distanceKm: 8,
    nameHit: true,
    canDo: '观察温室和灌溉',
    accessStatus: 'verified-public',
  },
  {
    name: '农业科技办公楼',
    distanceKm: 3,
    semanticScore: 0.2,
    accessStatus: 'unverified',
  },
  {
    name: '远郊农场',
    distanceKm: 55,
    nameHit: true,
  },
], { travel });
assert.equal(ranked[0].name, '现代农业示范园');
assert.equal(ranked[0].tier, 'A');
assert.equal(ranked.at(-1).tier, 'C');

const promptText = await fs.readFile(new URL('../functions/_lib/pbl-prompts.js', import.meta.url), 'utf8');
assert.match(promptText, /placeRequirement/);
assert.match(promptText, /campusOnly/);
assert.match(promptText, /不编造场馆专名/);
const evalSource = await fs.readFile(new URL('./pbl-place-jev-eval.mjs', import.meta.url), 'utf8');
assert.match(evalSource, /JEV_THRESHOLD = 0\.35/);
const analyzeSource = await fs.readFile(new URL('../functions/api/pbl/analyze.js', import.meta.url), 'utf8');
assert.match(analyzeSource, /stage === 'verify-places'[\s\S]*logPBLCall/);

const request = new Request('https://www.teachany.cn/api/pbl/places', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    place: { landmark: '模拟学校', lat: 22.55, lon: 114.05 },
    goal: '做一个交换校服的小程序',
    requirement: {
      campusOnly: true,
      reason: '可在校园内完成',
      queryGroups: [],
    },
    travel: { limitMinutes: 60 },
  }),
});
const response = await placesPost({ request, env: {} });
assert.equal(response.status, 200);
const body = await response.json();
assert.equal(body.reason, 'campus');
assert.equal(body.requirement.campusOnly, true);
assert.equal(body.travel.limitMinutes, 60);
assert.equal(body.travel.radiusKm, 30);
assert.equal(body.center.confidence, 'high');

const originalFetch = globalThis.fetch;
globalThis.fetch = async (input) => {
  const url = String(input);
  if (url.includes('overpass')) {
    return new Response(JSON.stringify({ elements: [] }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }
  if (url.includes('photon.komoot.io')) {
    return new Response(JSON.stringify({
      features: [
        {
          properties: { name: '现代农业示范农场', osm_key: 'landuse', osm_value: 'farmland' },
          geometry: { coordinates: [114.08, 22.57] },
        },
        {
          properties: { name: '深圳机场', osm_key: 'aeroway', osm_value: 'aerodrome' },
          geometry: { coordinates: [113.82, 22.64] },
        },
        {
          properties: { name: '农业银行大厦', osm_key: 'office', osm_value: 'financial' },
          geometry: { coordinates: [114.01, 22.55] },
        },
      ],
    }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  }
  if (url.includes('nominatim.openstreetmap.org')) {
    return new Response(JSON.stringify([{
      display_name: '南山区, 深圳市, 广东省, 中国',
      lon: '113.9256',
      lat: '22.5360',
    }]), { status: 200, headers: { 'Content-Type': 'application/json' } });
  }
  throw new Error(`unexpected fetch ${url}`);
};
try {
  const fieldRequest = new Request('https://www.teachany.cn/api/pbl/places', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      place: { landmark: '模拟学校', lat: 22.55, lon: 114.05 },
      goal: '现代农业调查',
      requirement: {
        campusOnly: false,
        object: '现代农业',
        see: ['温室和农作物'],
        evidence: ['种植记录'],
        activities: ['观察'],
        queryGroups: [{ keywords: ['农场'], types: ['farm'], priority: 1 }],
      },
      travel: { limitMinutes: 60, preferredMinutes: 45 },
    }),
  });
  const fieldResponse = await placesPost({ request: fieldRequest, env: {} });
  assert.equal(fieldResponse.status, 200);
  const fieldBody = await fieldResponse.json();
  assert.equal(fieldBody.routeSource, 'fixed-radius');
  assert.equal(fieldBody.candidates[0].name, '现代农业示范农场');
  assert.equal(fieldBody.candidates.some(item => /机场|银行/.test(item.name)), false);
  assert.equal(fieldBody.candidates[0].rangeShape, 'parallelogram');
  assert.equal(fieldBody.area.radiusKm, 30);
  assert.ok(fieldBody.warnings.some(item => item.includes('平行四边形')));

  const fallbackRequest = new Request('https://www.teachany.cn/api/pbl/places', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      place: {
        province: '广东省',
        city: '深圳市',
        district: '南山区',
        landmark: '地图中不存在的测试学校',
      },
      goal: '现代农业调查',
      requirement: {
        campusOnly: false,
        object: '现代农业',
        queryGroups: [{ keywords: ['农场'], types: ['farm'], priority: 1 }],
      },
    }),
  });
  const fallbackResponse = await placesPost({ request: fallbackRequest, env: {} });
  const fallbackBody = await fallbackResponse.json();
  assert.equal(fallbackResponse.status, 200);
  assert.equal(fallbackBody.center.approximate, true);
  assert.equal(fallbackBody.center.confidence, 'low');
  assert.ok(fallbackBody.warnings.some(item => item.includes('未精确定位学校')));
} finally {
  globalThis.fetch = originalFetch;
}

console.log('pbl-place-system tests passed');
