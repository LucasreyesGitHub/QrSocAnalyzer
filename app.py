import os
import base64
import requests
from flask import Flask, render_template, request
from pyzbar.pyzbar import decode
from PIL import Image
from urllib.parse import urlparse

app = Flask(__name__)

# 🔑 CONFIGURACIÓN DE SEGURIDAD
# En local puedes poner tu key aquí: VT_API_KEY = "tu_key"
# En Render, esto leerá la variable de entorno automáticamente
# Cámbiala TEMPORALMENTE por esta:
T_API_KEY = os.environ.get("VT_API_KEY")

def analyze_security(url):
    """
    Combina inteligencia de VirusTotal con reglas heurísticas de SOC.
    """
    url_lower = url.lower()
    parsed = urlparse(url)
    domain = parsed.netloc if parsed.netloc else "Dominio desconocido"
    protocol = parsed.scheme.upper() if parsed.scheme else "N/A"
    
    # --- 1. Lógica Heurística Interna ---
    is_https = url_lower.startswith("https")
    is_shortener = any(s in url_lower for s in ["bit.ly", "t.co", "goo.gl", "tinyurl", "rb.gy", "cutt.ly"])
    suspicious_keywords = ["login", "verify", "secure", "bank", "update", "account"]
    has_keywords = any(key in url_lower for key in suspicious_keywords)

    # --- 2. Consulta a VirusTotal API v3 ---
    vt_level = "UNKNOWN"
    vt_msg = "No hay registros previos en la base de datos de VirusTotal."
    
    if VT_API_KEY:
        try:
            # Codificar URL para API de VirusTotal
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
            headers = {"x-apikey": VT_API_KEY}
            
            response = requests.get(api_url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                stats = response.json()['data']['attributes']['last_analysis_stats']
                malicious = stats.get('malicious', 0)
                suspicious = stats.get('suspicious', 0)
                
                if malicious > 0:
                    vt_level = "CRITICAL"
                    vt_msg = f"🚨 ALERTA SOC: {malicious} motores de antivirus confirman que este link es MALICIOSO."
                elif suspicious > 0:
                    vt_level = "WARNING"
                    vt_msg = "⚠️ PRECAUCIÓN: Motores de seguridad marcan este enlace como sospechoso."
                else:
                    vt_level = "SECURE"
                    vt_msg = "✅ VirusTotal confirma que este enlace no tiene amenazas reportadas."
        except Exception as e:
            vt_msg = f"Error conectando con VirusTotal: {str(e)}"
    else:
        vt_msg = "Análisis de VirusTotal no disponible (Falta API Key)."

    # --- 3. Veredicto Final Basado en Prioridades ---
    # Prioridad 1: Detección confirmada por Antivirus
    if vt_level == "CRITICAL":
        return {"level": "CRITICAL", "score": "95/100", "comment": vt_msg, "domain": domain, "protocol": protocol}
    
    # Prioridad 2: Links acortados (Altamente sospechosos en QRs)
    if is_shortener:
        return {"level": "WARNING", "score": "75/100", "comment": f"⚠️ RIESGO: {vt_msg} Además, utiliza un acortador que oculta el destino real.", "domain": domain, "protocol": protocol}
    
    # Prioridad 3: Falta de cifrado
    if not is_https:
        return {"level": "WARNING", "score": "50/100", "comment": "⚠️ RIESGO MEDIO: El sitio no usa HTTPS. La información enviada no es privada.", "domain": domain, "protocol": protocol}

    # Prioridad 4: Confirmado seguro por VT
    if vt_level == "SECURE":
        return {"level": "SECURE", "score": "10/100", "comment": vt_msg, "domain": domain, "protocol": protocol}

    # Prioridad 5: Caso por defecto (Link nuevo pero estructura limpia)
    return {"level": "LOW_RISK", "score": "30/100", "comment": "ℹ️ El link es nuevo y no tiene reportes, pero usa HTTPS. Procede con cautela.", "domain": domain, "protocol": protocol}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                img = Image.open(file)
                decoded_objects = decode(img)
                
                if decoded_objects:
                    url = decoded_objects[0].data.decode('utf-8')
                    # Ejecutar análisis completo
                    analysis = analyze_security(url)
                    result = {
                        "status": "SUCCESS",
                        "url": url,
                        **analysis
                    }
                else:
                    result = {"status": "ERROR", "message": "No se detectó ningún código QR en la imagen."}
            except Exception as e:
                result = {"status": "ERROR", "message": f"Error del sistema: {str(e)}"}
                
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Configuración para Render (puerto 10000) o Local (puerto 5000/10000)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)

#Fin del codigo

