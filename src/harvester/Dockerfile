FROM python:3.10-slim

# Actualización de imagen para eliminar avisos de deprecación
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalación de dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente
COPY . .

# Comando por defecto
CMD ["python", "downloader.py"]