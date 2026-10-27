/**
 * Open Break OS — Service Worker (V8.1.1)
 * High-performance Cache-First Strategy for Offline Boutique Studio Access
 */
const CACHE_NAME = 'openbreak-v8-1-1-cache';
const CRITICAL_ASSETS = [
  './',
  './index.html',
  './landing_melius_style.html',
  './docs.html',
  './site.webmanifest',
  './assets/three.min.js',
  './assets/GLTFLoader.js',
  './assets/reformer_studio.glb',
  './assets/optimized/studio_hero.webp',
  './assets/optimized/coach_guiding.webp',
  './assets/optimized/class_action.webp',
  './assets/optimized/reformer_close.webp',
  './src/js/demo-store.js',
  './src/js/schedule-sync.js',
  './src/js/title-typewriter.js',
  './src/js/hero-tunnel.js',
  './src/js/motion-director.js',
  './src/js/analytics-engine.js',
  './src/js/scroll-choreography.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CRITICAL_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).catch(() => {
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
