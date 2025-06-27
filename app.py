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

# Ruta del chatbot con contexto
@app.route('/respuesta', methods=['POST'])
def respuesta():
    mensaje_usuario = request.json.get("mensaje")
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return jsonify({"respuesta": "Falta la API KEY de OpenRouter"}), 500

    # Inicializa historial si no existe
    if 'historial' not in session:
        session['historial'] = [{"role": "system", "content": "Eres un guía experto del Museo Nacional de Arte que contesta preguntas de los visitantes."}]

    # Añadir mensaje del usuario
    session['historial'].append({"role": "user", "content": mensaje_usuario})

    try:
        respuesta_api = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral/mistral-7b-instruct",
                "messages": session['historial']
            }
        )

        datos = respuesta_api.json()

        if "choices" not in datos:
            return jsonify({"respuesta": "Error en la respuesta del modelo"}), 500

        contenido_respuesta = datos["choices"][0]["message"]["content"]
        session['historial'].append({"role": "assistant", "content": contenido_respuesta})

        return jsonify({"respuesta": contenido_respuesta})

    except Exception as e:
        return jsonify({"respuesta": f"Error al conectar con OpenRouter: {str(e)}"}), 500
