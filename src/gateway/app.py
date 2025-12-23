from flask import Flask, render_template, send_from_directory, jsonify
import os
import json
import time

app = Flask(__name__)

# Ruta de almacenamiento definida en el NSR
DOWNLOADS_PATH = os.getenv('BASE_STORAGE_PATH', '/app/downloads')

def get_stats():
    stats_path = os.path.join(DOWNLOADS_PATH, 'stats.json')
    if os.path.exists(stats_path):
        with open(stats_path, 'r') as f:
            return json.load(f)
    return {}

@app.route('/')
def index():
    # Listamos los directorios (usuarios) en la base de datos local
    usuarios = [d for d in os.listdir(DOWNLOADS_PATH) if os.path.isdir(os.path.join(DOWNLOADS_PATH, d))]
    stats = get_stats()
    return render_template('index.html', usuarios=usuarios, stats=stats)

@app.route('/user/<user_id>')
def list_songs(user_id):
    user_path = os.path.join(DOWNLOADS_PATH, user_id)
    if not os.path.exists(user_path):
        return "Usuario no encontrado", 404
    
    # Filtramos solo archivos .opus (nuestro estándar de oro rural)
    songs = [f for f in os.listdir(user_path) if f.endswith('.opus')]
    return render_template('songs.html', user_id=user_id, songs=songs)

@app.route('/stream/<user_id>/<filename>')
def stream_song(user_id, filename):
    # Entrega directa del archivo para streaming o descarga
    return send_from_directory(os.path.join(DOWNLOADS_PATH, user_id), filename)

@app.route('/request_update', methods=['POST'])
def request_update():
    config_dir = '/app/config'
    trigger_path = os.path.join(config_dir, 'trigger.json')
    
    # Salvaguarda: Crear el directorio si no existe
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        
    with open(trigger_path, 'w') as f:
        json.dump({"trigger": True, "timestamp": time.time()}, f)
    
    return jsonify({"status": "Cosecha solicitada al NSR"}), 202

if __name__ == '__main__':
    # El NSR opera en el puerto 5000 para el panel de control
    app.run(host='0.0.0.0', port=5000, debug=True)