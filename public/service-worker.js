const CACHE = 'familia-en-juego-cloud-v4';
const ASSETS = ['/', '/tv', '/?join=1', '/styles.css', '/bomb.css', '/i18n.js', '/app.js', '/manifest.webmanifest', '/icons/icon-192.png', '/icons/icon-512.png', '/icons/apple-touch-icon.png', '/images/family-hero.webp', '/images/games/trivia.webp', '/images/games/mimica.webp', '/images/games/dibujo.webp', '/images/games/rapido.webp', '/images/games/quien_dijo.webp', '/images/games/quien_soy.webp', '/images/games/tres_verdades.webp', '/images/games/just_sing.webp', '/images/games/incognito.webp', '/images/games/bomba.webp'];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key)))));
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET' || new URL(event.request.url).pathname.startsWith('/api/')) return;
  event.respondWith(fetch(event.request).then(response => {
    const copy = response.clone();
    caches.open(CACHE).then(cache => cache.put(event.request, copy));
    return response;
  }).catch(() => caches.match(event.request)));
});
