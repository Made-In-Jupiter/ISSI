from flask import Flask, render_template, request, jsonify, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'clave-supersecreta'

# Ruta raíz
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/qr')
def qr():
    return render_template("qr.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/respuesta', methods=['POST'])
def respuesta():
    mensaje_usuario = request.json.get("mensaje")
    
    # Puedes poner aquí tu API Key directamente para pruebas locales
    api_key = "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"

    instrucciones = [
        "Eres un guía experto del Museo de Arte Moderno.",
        "Responde con claridad, pocas palabras y tono amable.",
        "Puedes responder sobre: ubicación, precios, horarios, disponibilidad y datos del museo, sí solo sí eres preguntado sobre ello.",
        "Si no sabes algo, responde con sinceridad y evita inventar.",
        "No hables de política, medicina ni temas no relacionados al museo.",
        "Evita repetir frases innecesarias como 'como modelo de lenguaje...'."
    ]
    
    system_prompt = "\n".join(instrucciones)
    
    mensajes = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": mensaje_usuario}
    ]

    try:
        respuesta_api = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": mensajes
            }
        )

        if respuesta_api.status_code == 200:
            contenido = respuesta_api.json()["choices"][0]["message"]["content"]
            return jsonify({"respuesta": contenido})
        else:
            return jsonify({"respuesta": f"Error {respuesta_api.status_code}: {respuesta_api.text}"}), 500

    except Exception as e:
        return jsonify({"respuesta": f"Error al conectar con OpenRouter: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)