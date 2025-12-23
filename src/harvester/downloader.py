import os
import json
import yt_dlp
import logging
import time

# Configuración de logs para el Observador
logging.basicConfig(level=logging.INFO, format='O.R.I.O.N. > %(message)s')

def cargar_configuracion():
    path = '/app/config/users_config.json'
    if not os.path.exists(path):
        logging.error("No se encontró el archivo de configuración.")
        return None
    with open(path, 'r') as f:
        return json.load(f)

def cosechar_musica():
    config = cargar_configuracion()
    if not config: return

    base_path = os.getenv('BASE_STORAGE_PATH', '/app/downloads')
    
    # Opciones de yt-dlp: Optimización Rural (Opus/AAC)
    ydl_opts_base = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': config['config_global'].get('formato_preferido', 'opus'),
            'preferredquality': '128',
        }],
        'ignoreerrors': True,
        'no_overwrites': True,
        # El archivo de registro evita descargar lo que ya existe (Sincronización Diferencial)
        'download_archive': os.path.join(base_path, 'archive.log'),
    }

    for usuario in config['usuarios']:
        user_id = usuario['id']
        logging.info(f"Iniciando cosecha para: {usuario['nombre']} ({user_id})")
        
        for playlist_url in usuario['playlists']:
            opts = ydl_opts_base.copy()
            # Organización jerárquica: /app/downloads/user_id/nombre_cancion.ext
            opts['outtmpl'] = f"{base_path}/{user_id}/%(title)s.%(ext)s"
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([playlist_url])

if __name__ == "__main__":
    # Extraemos el intervalo de la configuración (convertido a segundos)
    config = cargar_configuracion()
    intervalo = config['config_global'].get('intervalo_sincronizacion_horas', 6) * 3600
    
    logging.info(f"Motor Harvester activado. Ciclo de órbita: cada {intervalo/3600} horas.")
    
    while True:
        cosechar_musica()
        logging.info(f"Ciclo completado. Entrando en hibernación por {intervalo/3600} horas...")
        # El script se mantiene vivo, pero en reposo, estabilizando el Eje H
        time.sleep(intervalo)