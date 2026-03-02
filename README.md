# 🔍 QrSocAnalyzer - VirusTotal Integrated

**QrSocAnalyzer** es una herramienta de análisis de seguridad diseñada para decodificar códigos QR y realizar un escaneo instantáneo de las URLs contenidas utilizando la API de **VirusTotal**. 

Este proyecto está enfocado en prevenir ataques de **QRishing** (QR Phishing), permitiendo a los analistas de SOC y usuarios finales verificar la reputación de un enlace antes de visitarlo.

## ✨ Características
* **Decodificación QR:** Extrae URLs de imágenes cargadas (soporta PNG, JPG, JPEG).
* **Análisis de Reputación:** Consulta en tiempo real la base de datos de VirusTotal.
* **Indicadores Visuales:** Alertas en rojo para enlaces maliciosos y verde para sitios limpios.
* **Despliegue en la Nube:** Configurado para funcionar en entornos Docker (Render, AWS, etc.).

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.11
* **Framework Web:** Flask
* **Procesamiento de Imágenes:** Pillow & PyZbar
* **Integración de Seguridad:** VirusTotal API v3
* **Servidor de Producción:** Gunicorn
* **Contenedor:** Docker (Debian-slim)

## 🚀 Instalación y Uso Local

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/LucasreyesGitHub/QrSocAnalyzer.git](https://github.com/LucasreyesGitHub/QrSocAnalyzer.git)
    cd QrSocAnalyzer
    ```

2.  **Configurar variables de entorno:**
    Crea un archivo `.env` o exporta tu clave de API:
    ```bash
    export VT_API_KEY="tu_clave_de_virustotal_aqui"
    ```

3.  **Ejecutar con Docker (Recomendado):**
    ```bash
    docker build -t qrsocanalyzer .
    docker run -p 10000:10000 -e VT_API_KEY=$VT_API_KEY qrsocanalyzer
    ```

4.  **Acceder:** Abre `http://localhost:10000` en tu navegador.

## 🌐 Despliegue en Render
Para que la librería `zbar` funcione correctamente en Render, se utiliza el **Dockerfile** incluido. 

**Configuración necesaria en Render:**
1.  **Runtime:** Docker
2.  **Environment Variable:** * `VT_API_KEY`: Tu clave privada de VirusTotal.

## 🛡️ Uso en SOC
Esta herramienta es ideal para flujos de triaje inicial donde se sospecha de códigos QR recibidos por correo electrónico o encontrados en espacios físicos.

---
Desarrollado por [Lucas Reyes](https://github.com/LucasreyesGitHub)
