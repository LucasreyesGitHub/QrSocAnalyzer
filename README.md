# 🛡️ QR SOC Analyzer

![Status](https://img.shields.io/badge/Status-Live-success)
![Platform](https://img.shields.io/badge/Deployed-Render-blue)
![Tech](https://img.shields.io/badge/Tech-Python_|_Flask_|_Docker-lightgrey)

**QR SOC Analyzer** es una herramienta de ciberseguridad diseñada para mitigar el *Quishing* (Phishing a través de códigos QR). La aplicación permite cargar una imagen de un código QR, decodificar su contenido y realizar un análisis de reputación técnico bajo un formato de reporte estilo **SOC (Security Operations Center)**.

---

## 🚀 Proceso de Funcionamiento

El flujo de la aplicación sigue estos pasos técnicos:

1.  **Ingesta de Datos:** El usuario carga una imagen (PNG/JPG) a través de la interfaz minimalista.
2.  **Decodificación (Engine):** El sistema utiliza el motor de **PyZbar** para localizar y extraer la cadena de texto/URL oculta en el código QR.
3.  **Análisis de Seguridad:** Una vez extraída la URL, el backend procesa la cadena buscando:
    * **Protocolo:** Verificación de cifrado SSL (HTTP vs HTTPS).
    * **Reputación de Dominio:** Detección de acortadores de URL (bit.ly, t.co, etc.) que suelen ocultar destinos maliciosos.
    * **Análisis de Patrones:** Identificación de palabras clave asociadas a Phishing (login, verify, secure).
4.  **Generación de Reporte:** Se devuelve un objeto JSON al frontend que renderiza un reporte con nivel de riesgo (CRITICAL, WARNING, SECURE) y un comentario en lenguaje natural para el usuario final.

---

## 🛠️ Utilidad para un SOC (Security Operations Center)

En un entorno corporativo o de monitoreo, esta herramienta sirve como:

* **Triage Rápido:** Permite a los analistas de Nivel 1 verificar enlaces sospechosos reportados por empleados sin exponer sus propios navegadores al riesgo.
* **Prevención de Quishing:** Educa al usuario final traduciendo tecnicismos (como la falta de HTTPS o el uso de acortadores) en advertencias claras y accionables.
* **Análisis de Vectores de Ataque:** Ayuda a documentar cómo se están distribuyendo enlaces maliciosos dentro de una organización mediante soportes físicos.

---

## 🌐 Despliegue

La aplicación está desplegada en **Render** utilizando contenedores **Docker** para garantizar la estabilidad de las librerías de sistema (`libzbar0`).

* **Repositorio:** [https://github.com/LucasreyesGitHub/QrSocAnalyzer]
* **URL de Producción:** [https://qrsocanalyzer.onrender.com/]

---

## 📦 Instalación Local

Si deseas ejecutar este proyecto localmente:

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/TuUsuario/QrSocAnalyzer.git](https://github.com/LucasreyesGitHu/QrSocAnalyzer.git)
