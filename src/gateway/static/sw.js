const CACHE_NAME = 'orion-nebula-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/style.css', // Si decidió separar el CSS
    '/static/icons/icon.png' // Opcional para el logo
];

// Instalación: Guardamos la interfaz base en la memoria del dispositivo
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

// Estrategia: Network First, falling back to Cache
// Priorizamos la red para música nueva, pero servimos la UI si hay desconexión
self.addEventListener('fetch', (event) => {
    event.respondWith(
        fetch(event.request).catch(() => {
            return caches.match(event.request);
        })
    );
});