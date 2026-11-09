// Offline support: app shell is cached; map tiles you have viewed are cached as you browse.
const SHELL = 'shell-20261109140642', TILES = 'tiles-v1';
const ASSETS = ['./', 'index.html', 'schedule.json', 'manifest.json', 'icon-180.png', 'icon-192.png', 'icon-512.png',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css', 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => Promise.all(ASSETS.map(u => c.add(new Request(u, {mode: u.startsWith('http') ? 'cors' : 'same-origin'})).catch(() => {})))));
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('shell-') && k !== SHELL).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (/arcgisonline\.com|tile\.openstreetmap\.org/.test(u.host)) {         // tiles: cache first
    e.respondWith(caches.open(TILES).then(async c => {
      const hit = await c.match(e.request); if (hit) return hit;
      const r = await fetch(e.request); if (r.ok || r.type === 'opaque') { c.put(e.request, r.clone()); trim(c); } return r;
    }).catch(() => caches.match(e.request)));
    return;
  }
  // app files: network first (so updates arrive), cache fallback when offline
  e.respondWith(fetch(e.request).then(r => { if (r.ok && (u.origin === location.origin || u.host === 'unpkg.com')) caches.open(SHELL).then(c => c.put(e.request, r.clone())); return r; })
    .catch(() => caches.match(e.request, {ignoreSearch: true}).then(r => r || caches.match('index.html'))));
});
let trimming = false;
async function trim(c) { if (trimming) return; trimming = true;
  const ks = await c.keys(); for (let i = 0; i < ks.length - 2500; i++) await c.delete(ks[i]); trimming = false; }
