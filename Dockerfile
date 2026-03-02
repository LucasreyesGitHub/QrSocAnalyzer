# Usa una imagen oficial de Python
FROM python:3.11-slim

# INSTALA LA LIBRERÍA DEL SISTEMA QUE FALTA (ZBAR)
RUN apt-get update && apt-get install -y \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto que usa Render
EXPOSE 10000

# Comando para arrancar la app con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]