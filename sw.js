const CACHE = 'roseto-eventi-v7';
const ASSETS = [
  '/roseto-eventi/',
  '/roseto-eventi/index.html',
  '/roseto-eventi/manifest.json',
  '/roseto-eventi/favicon.svg'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method === 'GET' && url.origin === self.location.origin && (url.pathname.endsWith('/data/events.json') || url.pathname.endsWith('/data/sagre.json'))) {
    e.respondWith(
      fetch(e.request).then(res => {
        if (!res.ok) return res;
        const clone = res.clone();
        return caches.open(CACHE)
          .then(cache => cache.put(e.request, clone))
          .catch(() => undefined)
          .then(() => res);
      }).catch(() => caches.match(e.request))
    );
    return;
  }
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
      if (res.ok && e.request.method === 'GET' && e.request.url.startsWith(self.location.origin)) {
        const clone = res.clone();
        return caches.open(CACHE)
          .then(cache => cache.put(e.request, clone))
          .catch(() => undefined)
          .then(() => res);
      }
      return res;
    }).catch(() => caches.match('/roseto-eventi/')))
  );
});

self.addEventListener('push', e => {
  let data = { title: '📅 Eventi Roseto', body: 'Nuovi eventi disponibili!' };
  if (e.data) {
    try { data = e.data.json(); } catch { data.body = e.data.text(); }
  }
  e.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/roseto-eventi/icon-192.png',
      badge: '/roseto-eventi/icon-192.png',
      vibrate: [200, 100, 200],
      data: { url: '/roseto-eventi/' }
    })
  );
});

self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = e.notification.data?.url || '/roseto-eventi/';
  e.waitUntil(clients.openWindow(url));
});
