FROM python:3.10-slim

# Instalamos librerías de sistema
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Render requiere el puerto 10000 por defecto
ENV PORT=10000

# Ejecutamos gunicorn apuntando al archivo app y a la variable app
CMD gunicorn --bind 0.0.0.0:$PORT app:app