# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Instalamos las librerías de sistema necesarias (libzbar0)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos del proyecto
COPY . .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para arrancar la app con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]