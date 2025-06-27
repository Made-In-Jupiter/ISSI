import os
import requests

# ⚠️ Pega tu API KEY aquí directamente (solo para pruebas)
api_key = "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"

# Plantilla de directivas para el modelo (formato guía del museo)
instrucciones = [
    "Eres un guía experto del Museo de Arte Moderno.",
    "Responde con claridad, pocas palabras y tono amable.",
    "Puedes responder sobre: ubicación, precios, horarios, disponibilidad y datos del museo, sí solo sí eres preguntado sobre ello.",
    "Si no sabes algo, responde con sinceridad y evita inventar.",
    "No hables de política, medicina ni temas no relacionados al museo.",
    "Evita repetir frases innecesarias como 'como modelo de lenguaje...'."
]

# Construir un solo mensaje system con todas las directivas
system_prompt = "\n".join(instrucciones)

# Mensaje de prueba del usuario
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Qué obras de Diego Rivera tienen?"}
]

# Llamada a la API de OpenRouter
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "mistralai/mistral-7b-instruct",
        "messages": messages
    }
)

# Mostrar la respuesta
if response.status_code == 200:
    content = response.json()["choices"][0]["message"]["content"]
    print("✅ Éxito. Respuesta del modelo:")
    print(content)
else:
    print("❌ Error:", response.status_code)
    print(response.text)
