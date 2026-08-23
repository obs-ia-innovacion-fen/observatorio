"""
Descubre la URL real del feed RSS/Atom de un sitio.

Dos estrategias: primero lee la portada y busca la etiqueta <link rel="alternate">
que los sitios usan para declarar su feed, que es el metodo confiable. Si no la
encuentra, prueba las rutas convencionales.

Uso:  python scripts/buscar_feeds.py https://www.brookings.edu
      python scripts/buscar_feeds.py https://oecd.ai https://www.cepal.org
"""

import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

AGENTE = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0 Safari/537.36 ObservatorioFEN/1.0 (jeosepulve@fen.uchile.cl)"
)

RUTAS = ("/feed/", "/rss", "/rss.xml", "/feed.xml", "/atom.xml",
         "/index.xml", "/rss/all.xml", "/en/rss.xml")


def pedir(url, limite=400_000):
    solicitud = urllib.request.Request(url, headers={
        "User-Agent": AGENTE,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/html, */*",
    })
    with urllib.request.urlopen(solicitud, timeout=20) as respuesta:
        return respuesta.read(limite)


def es_feed(datos):
    try:
        raiz = ET.fromstring(datos)
    except ET.ParseError:
        return False
    etiqueta = raiz.tag.lower()
    return "rss" in etiqueta or "feed" in etiqueta or raiz.find("channel") is not None


def declarados_en_portada(base):
    """Los sitios bien hechos declaran su feed en el <head> de la portada."""
    try:
        html = pedir(base).decode("utf-8", "ignore")
    except Exception as error:
        print(f"  no se pudo leer la portada: {error}")
        return []

    encontrados = []
    for etiqueta in re.findall(r"<link[^>]+>", html, re.IGNORECASE):
        if "alternate" not in etiqueta.lower():
            continue
        if not re.search(r"application/(rss|atom)\+xml", etiqueta, re.IGNORECASE):
            continue
        href = re.search(r'href=["\']([^"\']+)["\']', etiqueta, re.IGNORECASE)
        if href:
            encontrados.append(urllib.parse.urljoin(base, href.group(1)))
    return encontrados


def revisar(base):
    base = base.rstrip("/")
    print(f"\n{base}")

    candidatos = declarados_en_portada(base)
    if candidatos:
        print(f"  declarados en la portada: {len(candidatos)}")
    candidatos += [base + ruta for ruta in RUTAS]

    vistos, hallazgos = set(), []
    for url in candidatos:
        if url in vistos:
            continue
        vistos.add(url)
        try:
            datos = pedir(url)
        except Exception:
            continue
        if es_feed(datos):
            hallazgos.append(url)
            print(f"  FEED -> {url}")

    if not hallazgos:
        print("  sin feed detectado: revisar el pie de pagina del sitio a mano")
    return hallazgos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    for base in sys.argv[1:]:
        revisar(base)


if __name__ == "__main__":
    main()
