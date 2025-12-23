import time
import os
import json
import yt_dlp
import logging
import shutil
import glob

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
        
        # --- NUEVA LÓGICA DE LIMPIEZA DE RESIDUOS ---
        ruta_usuario = os.path.join(base_path, usuario['id'])
        # Buscamos archivos de imagen que ya no necesitamos tras la incrustación
        for imagen_residual in glob.glob(f"{ruta_usuario}/*.jpg") + \
                               glob.glob(f"{ruta_usuario}/*.webp") + \
                               glob.glob(f"{ruta_usuario}/*.png"):
            try:
                os.remove(imagen_residual)
                logging.info(f"Residuo eliminado: {os.path.basename(imagen_residual)}")
            except Exception as e:
                logging.warning(f"No se pudo eliminar el residuo {imagen_residual}: {e}")
    
    actualizar_stats(base_path)

def check_trigger():
    path = '/app/config/trigger.json'
    if os.path.exists(path):
        os.remove(path) # Consumimos la señal
        return True
    return False

if __name__ == "__main__":
    config = cargar_configuracion()
    intervalo_base = config['config_global'].get('intervalo_sincronizacion_horas', 6) * 3600
    ultimo_check = 0

    while True:
        ahora = time.time()
        # Se activa por tiempo O por petición del usuario
        if ahora - ultimo_check > intervalo_base or check_trigger():
            logging.info("Señal detectada o ciclo cumplido. Iniciando transmutación...")
            cosechar_musica()
            ultimo_check = ahora
        
        time.sleep(30) # El motor vigila la señal cada 30 seg