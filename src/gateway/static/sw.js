const CACHE_NAME = 'orion-nebula-v1';
const MUSIC_CACHE = 'orion-music-v1';

// Recursos de la Interfaz (UI)
const ASSETS_TO_CACHE = [
    '/',
    '/static/style.css'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
    );
});

self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Estrategia especial para archivos de música (.opus)
    if (url.pathname.endsWith('.opus')) {
        event.respondWith(
            caches.open(MUSIC_CACHE).then((cache) => {
                return cache.match(event.request).then((response) => {
                    // Si ya está en caché, lo servimos instantáneamente
                    if (response) return response;

                    // Si no, lo buscamos en la red y lo guardamos para la próxima vez
                    return fetch(event.request).then((networkResponse) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                });
            })
        );
    } else {
        // Estrategia estándar para la Interfaz (UI)
        event.respondWith(
            caches.match(event.request).then((response) => {
                return response || fetch(event.request);
            })
        );
    }
});