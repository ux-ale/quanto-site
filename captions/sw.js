// Shell cache for the captions page. Launching from the home screen was
// refetching everything over the network each time; serving from cache
// makes it paint immediately, online or not.
//
// Bump CACHE whenever the shell changes.
const CACHE = 'quanto-captions-v1';
const SHELL = [
  './',
  './index.html',
  './sora-latin.woff2',
  './quanto-icon-192.png',
  './manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Serve from cache at once, then refresh it in the background, so a launch
// never waits on the network and the next one picks up any redeploy.
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;

  e.respondWith(
    caches.open(CACHE).then(cache =>
      cache.match(req).then(hit => {
        const fresh = fetch(req)
          .then(res => {
            if (res && res.ok) cache.put(req, res.clone());
            return res;
          })
          .catch(() => hit);
        return hit || fresh;
      })
    )
  );
});
