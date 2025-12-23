FROM python:3.10-slim

WORKDIR /app

# Instalación de librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la lógica del Gateway
COPY . .

# Comando de inicio del servidor web
CMD ["python", "app.py"]