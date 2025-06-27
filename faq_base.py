from sentence_transformers import SentenceTransformer
import numpy as np

# Modelo para vectorizar preguntas
modelo = SentenceTransformer('all-MiniLM-L6-v2')

# Base de preguntas frecuentes y respuestas
faq = [
    ("¿Dónde está ubicado el museo?", "El museo está ubicado en Reforma y Gandhi s/n, Bosque de Chapultepec, Ciudad de México."),
    ("¿Cuál es el horario del museo?", "Abre de martes a domingo, de 10:15 a 17:30. Cierra los lunes."),
    ("¿Cuánto cuesta la entrada?", "La entrada general cuesta $95. Hay entrada gratuita para menores de 13, estudiantes, maestros y adultos mayores con credencial."),
    ("¿Se permiten fotos?", "Sí, se permite tomar fotos sin flash ni tripié. Para video hay un costo adicional."),
    ("¿Qué artistas están en el museo?", "Hay obras de Siqueiros, Frida Kahlo, Diego Rivera y otros artistas modernos mexicanos."),
    ("¿Qué exposiciones hay?", "Las exposiciones varían. Puedes consultar la sección 'Exposiciones' en la página oficial del museo."),
    ("¿Se puede comprar boleto en línea?", "Sí, los boletos se pueden comprar en línea y también en taquilla."),
    ("¿El museo es accesible?", "Sí, el museo tiene acceso para personas con discapacidad.")
]

# Calcula embeddings
preguntas = [p for (p, r) in faq]
embeddings_faq = modelo.encode(preguntas)

def buscar_pregunta_similar(pregunta_usuario, umbral=0.7):
    vector_usuario = modelo.encode([pregunta_usuario])[0]
    similitudes = np.dot(embeddings_faq, vector_usuario) / (
        np.linalg.norm(embeddings_faq, axis=1) * np.linalg.norm(vector_usuario)
    )
    indice_max = np.argmax(similitudes)
    if similitudes[indice_max] >= umbral:
        return faq[indice_max][1]
    else:
        return None
