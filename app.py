import os
from flask import Flask, render_template, request
from pyzbar.pyzbar import decode
from PIL import Image
from urllib.parse import urlparse

app = Flask(__name__)

def analyze_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    protocol = parsed.scheme
    
    # Lógica de riesgo
    is_https = protocol == "https"
    is_shortener = domain in ["bit.ly", "t.co", "goo.gl", "tinyurl.com", "rb.gy"]
    
    if is_shortener:
        level = "CRITICAL"
        risk_score = "85/100"
        comment = "⚠️ Enlace acortado detectado. Estos links ocultan el destino real y son usados frecuentemente para estafas."
    elif not is_https:
        level = "WARNING"
        risk_score = "50/100"
        comment = "⚠️ El sitio no utiliza HTTPS. La información que envíes (contraseñas o datos) podría ser interceptada."
    else:
        level = "SECURE"
        risk_score = "10/100"
        comment = "✅ El enlace parece legítimo, utiliza cifrado SSL y no presenta patrones de riesgo conocidos."

    return {
        "level": level,
        "score": risk_score,
        "domain": domain if domain else "N/A",
        "protocol": protocol.upper() if protocol else "N/A",
        "comment": comment
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                img = Image.open(file)
                decoded = decode(img)
                if decoded:
                    url = decoded[0].data.decode('utf-8')
                    analysis = analyze_url(url)
                    result = {
                        "url": url,
                        "status": "SUCCESS",
                        **analysis
                    }
                else:
                    result = {"status": "ERROR", "message": "No se detectó código QR."}
            except Exception as e:
                result = {"status": "ERROR", "message": f"Fallo de sistema: {str(e)}"}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Render usa la variable de entorno PORT, si no existe usa el 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)