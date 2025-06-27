import re
import os
import json
import requests
from bs4 import BeautifulSoup

def obtener_urls_desde_html(ruta_html):
    with open(ruta_html, encoding="utf-8") as f:
        contenido = f.read()
    patron = r'href="(https://munal\.mx/en/exhibitions/[a-zA-Z0-9\-\%]+)"'
    coincidencias = re.findall(patron, contenido)
    return sorted(set(coincidencias))

def extraer_datos_exposicion(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"url": url, "error": "No se pudo acceder"}

    soup = BeautifulSoup(response.text, "html.parser")

    titulo = ""
    posibles_titulos = soup.find_all(["h1", "h2", "div", "span"])
    for tag in posibles_titulos:
        text = tag.get_text(strip=True)
        if len(text) > 10 and len(text.split()) >= 3 and "Exhibitions" not in text:
            titulo = text
            break
    if not titulo:
        titulo = "No encontrado"

    seccion = soup.find("main") or soup.find("section") or soup

    descripcion = ""
    for p in seccion.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 100:
            descripcion += text + "\n"

    texto_total = seccion.get_text(separator=" ").strip()
    fecha = ""
    match = re.search(r"\d{2} · \d{2} · \d{4}\s+—\s+\d{2} · \d{2} · \d{4}", texto_total)
    if match:
        fecha = match.group()
    else:
        match_simple = re.search(r"\d{2} · \d{2} · \d{4}", texto_total)
        if match_simple:
            fecha = match_simple.group()

    return {
        "url": url,
        "titulo": titulo,
        "fecha": fecha,
        "descripcion": descripcion.strip()
    }

def procesar_exposiciones(ruta_html, archivo_salida="exposiciones.json"):
    urls = obtener_urls_desde_html(ruta_html)
    resultados = [extraer_datos_exposicion(u) for u in urls]
    os.makedirs("salida", exist_ok=True)
    ruta_salida = os.path.join("salida", archivo_salida)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(resultados)} exposiciones guardadas en {ruta_salida}")
    return ruta_salida

if __name__ == "__main__":
    procesar_exposiciones("Museo Nacional de Arte.html")
