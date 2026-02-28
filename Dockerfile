FROM python:3.10-slim

# Solo instalamos libzbar0 que es la única que pyzbar necesita
RUN apt-get update && apt-get install -y \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Render requiere el puerto 10000
ENV PORT=10000

CMD gunicorn --bind 0.0.0.0:$PORT app:app