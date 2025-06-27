import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Verifica que tengas la API Key cargada
if not api_key:
    raise ValueError("❌ Falta OPENROUTER_API_KEY en .env")

# Mensajes de prueba
messages = [
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": "¿Cuál es la capital de Francia?"}
]

# Modelo válido actualizado
model_id = "mistralai/mistral-7b-instruct"

# Llamada a la API de OpenRouter
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": model_id,
        "messages": messages
    }
)

# Imprimir resultado
if response.status_code == 200:
    print("✅ Conexión exitosa:")
    content = response.json()["choices"][0]["message"]["content"]
    print("🧠 Respuesta del modelo:", content)
else:
    print("❌ Error:", response.status_code, response.text)
