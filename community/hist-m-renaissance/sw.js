// TeachAny hist-m-renaissance · Service Worker v1.1.0
const CACHE = 'teachany-renaissance-v1-1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './manifest.webmanifest',
  // Hero + 内置插画
  './assets/hist-m-renaissance-hero.png',
  './assets/illust-three-masterpieces.png',
  './assets/illust-luther-95-theses.png',
  // 艺术品（mention-means-image 基线 ④）
  './assets/artwork-mona-lisa.jpg',
  './assets/artwork-raphael-madonna.png',
  './assets/artwork-david.jpg',
  './assets/artwork-school-athens.jpg',
  // 真实地图（基线 ⑯）
  './assets/maps/hillshade.png',
  './assets/maps/boundaries.geojson',
  './assets/maps/places.geojson',
  // TTS 音频
  './tts/s01.mp3',
  './tts/s02.mp3',
  './tts/s03.mp3',
  './tts/s04.mp3',
  './tts/s05.mp3',
  './tts/s06.mp3',
  './tts/s07.mp3',
  // 外部 Leaflet（允许降级到网络）
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => {
      // 尽量缓存，Leaflet CDN 失败不阻塞
      return Promise.allSettled(ASSETS.map(a => cache.add(a)));
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(resp => {
        if (resp.ok) {
          const clone = resp.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone)).catch(() => {});
        }
        return resp;
      }).catch(() => new Response('离线状态，资源不可用', { status: 503, statusText: 'offline' }));
    })
  );
});
