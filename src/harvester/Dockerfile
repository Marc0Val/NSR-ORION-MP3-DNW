FROM python:3.10-slim

# Instalación de herramientas de sistema: FFmpeg (Audio) y AtomicParsley (Metadatos)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    atomicparsley \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalación de librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la lógica del Harvester
COPY . .

# Comando de inicio del motor
CMD ["python", "downloader.py"]