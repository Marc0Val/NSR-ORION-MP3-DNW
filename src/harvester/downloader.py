import time
import os
import json
import yt_dlp
import logging
import shutil

logging.basicConfig(level=logging.INFO, format='O.R.I.O.N. > %(message)s')

def cargar_configuracion():
    path = '/app/config/users_config.json'
    if not os.path.exists(path): return None
    with open(path, 'r') as f: return json.load(f)

def actualizar_stats(base_path):
    # Cálculo de espacio para telemetría (Eje H)
    total, used, free = shutil.disk_usage(base_path)
    stats = {
        "storage_used_gb": round(used / (2**30), 2),
        "storage_free_gb": round(free / (2**30), 2),
        "last_sync": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(os.path.join(base_path, 'stats.json'), 'w') as f:
        json.dump(stats, f, indent=4)
    logging.info(f"Telemetría actualizada: {stats['storage_used_gb']}GB en uso.")

def cosechar_musica():
    config = cargar_configuracion()
    if not config: return
    base_path = os.getenv('BASE_STORAGE_PATH', '/app/downloads')
    
    ydl_opts_base = {
        'format': 'bestaudio/best',
        'writethumbnail': True,  # Descarga la carátula
        'postprocessors': [
            {   # Extraer Audio y convertir a Opus
                'key': 'FFmpegExtractAudio',
                'preferredcodec': config['config_global'].get('formato_preferido', 'opus'),
                'preferredquality': '128',
            },
            {   # Insertar Metadatos (Artista, Título, etc.)
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {   # Incrustar la carátula en el archivo
                'key': 'EmbedThumbnail',
            }
        ],
        'ignoreerrors': True,
        'no_overwrites': True,
        'download_archive': os.path.join(base_path, 'archive.log'),
    }

    for usuario in config['usuarios']:
        logging.info(f"Sincronizando sector: {usuario['nombre']}")
        for playlist_url in usuario['playlists']:
            opts = ydl_opts_base.copy()
            opts['outtmpl'] = f"{base_path}/{usuario['id']}/%(title)s.%(ext)s"
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([playlist_url])
    
    actualizar_stats(base_path)

if __name__ == "__main__":
    config = cargar_configuracion()
    intervalo = config['config_global'].get('intervalo_sincronizacion_horas', 6) * 3600
    while True:
        logging.info("Iniciando ciclo de transmutación de datos...")
        cosechar_musica()
        logging.info(f"Hibernando por {intervalo/3600} horas...")
        time.sleep(intervalo)