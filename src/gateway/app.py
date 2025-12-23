from flask import Flask, render_template, send_from_directory, abort
import os

app = Flask(__name__)

# La ruta base se lee desde el entorno, apuntando a nuestra carpeta de descargas
BASE_MUSIC_PATH = os.getenv('BASE_STORAGE_PATH', '/app/downloads')

@app.route('/')
def index():
    """Lista los usuarios (carpetas) disponibles."""
    usuarios = [d for d in os.listdir(BASE_MUSIC_PATH) 
                if os.path.isdir(os.path.join(BASE_MUSIC_PATH, d))]
    return render_template('index.html', usuarios=usuarios)

@app.route('/user/<username>')
def user_playlist(username):
    """Muestra las canciones cosechadas para un usuario específico."""
    user_path = os.path.join(BASE_MUSIC_PATH, username)
    if not os.path.exists(user_path):
        abort(404)
    
    canciones = [f for f in os.listdir(user_path) if f.endswith('.opus')]
    return render_template('playlist.html', username=username, canciones=canciones)

@app.route('/download/<username>/<filename>')
def download_file(username, filename):
    """Envía el archivo para streaming o descarga directa."""
    return send_from_directory(os.path.join(BASE_MUSIC_PATH, username), filename)

if __name__ == '__main__':
    # El puerto 5000 será nuestra ventana al exterior
    app.run(host='0.0.0.0', port=5000)