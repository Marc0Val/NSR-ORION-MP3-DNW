FROM python:3.10-slim

WORKDIR /app

# Instalación de dependencias mínimas para mantener la agilidad del NSR
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# El código se mapeará vía volumen en docker-compose para desarrollo fluido
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]