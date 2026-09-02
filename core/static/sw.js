/**
 * YATRALENS Progressive Web App (PWA) Service Worker
 * ===================================================
 * Provides:
 * 1. Offline Caching of App Shell, Leaflet Maps, and Tailwind assets
 * 2. Dedicated /offline/ Emergency Hub Fallback when disconnected
 * 3. Offline Emergency SOS synchronization queue
 */

const CACHE_NAME = 'yatralens-pwa-v1.2';
const STATIC_ASSETS = [
  '/',
  '/packages/',
  '/emergency/',
  '/women-safety/',
  '/offline/',
  '/api/emergency/offline-bundle/',
  '/static/manifest.json',
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://cdn.jsdelivr.net/npm/chart.js'
];

// Install Event - Pre-cache core shell & offline hub
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[YATRALENS SW] Pre-caching offline emergency assets and core shell...');
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('[YATRALENS SW] Some static assets could not be cached immediately:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate Event - Clean up stale caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[YATRALENS SW] Removing old cache version:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - Network First with Cache Fallback and Offline Emergency Fallback
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // Skip POST, PUT, DELETE, and non-GET requests from cache
  if (request.method !== 'GET') {
    return;
  }

  // Handle navigation requests (HTML pages)
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Clone and store fresh copy in cache
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return response;
        })
        .catch(async () => {
          console.log('[YATRALENS SW] Network failed, searching cache for:', request.url);
          const cachedResponse = await caches.match(request);
          if (cachedResponse) {
            return cachedResponse;
          }
          // If not in cache, fallback to the offline emergency hub
          const offlineFallback = await caches.match('/offline/');
          if (offlineFallback) {
            return offlineFallback;
          }
          return new Response(
            '<html><body style="font-family:sans-serif;padding:2rem;text-align:center;"><h2>⚠️ You are Offline</h2><p>Please connect to internet or dial <b>112</b> for ERSS emergency.</p><a href="/offline/">Open Offline Hub</a></body></html>',
            { headers: { 'Content-Type': 'text/html' } }
          );
        })
    );
    return;
  }

  // Cache-first for CDN and static assets (images, stylesheets, scripts)
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(request).then((networkResponse) => {
        if (
          networkResponse &&
          networkResponse.status === 200 &&
          (url.origin === location.origin || url.hostname.includes('cdnjs') || url.hostname.includes('unpkg') || url.hostname.includes('googleapis'))
        ) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, responseToCache));
        }
        return networkResponse;
      }).catch((err) => {
        // If an API request fails offline, check if we have cached JSON
        console.warn('[YATRALENS SW] Asset fetch failed offline:', request.url);
      });
    })
  );
});

// Background Sync / Message Event for Offline SOS flush
self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'PING_SW') {
    event.ports[0].postMessage({ status: 'PWA_ACTIVE', cacheVersion: CACHE_NAME });
  }
});
