"""
Recolector de medios por RSS/Atom para el Observatorio.

Guarda solo titular, fecha, medio y enlace. No descarga ni almacena el cuerpo
de los articulos: son publicaciones comerciales con derechos reservados y el
resumen que se publique debe ser redaccion propia con enlace a la fuente.

Uso:  python scripts/medios.py
"""

import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MEDIOS = RAIZ / "fuentes" / "medios.yml"
BANDEJA = RAIZ / "fuentes" / "bandeja"
# Varios servidores de prensa cierran la conexion con clientes que no parecen
# navegador. Se mantiene el contacto del Observatorio dentro del identificador.
AGENTE = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0 Safari/537.36 ObservatorioFEN/1.0 (jeosepulve@fen.uchile.cl)"
)
MAX_POR_MEDIO = 20

# Los feeds de portada entran completos: obituarios, futbol, politica general.
# Un titular se conserva solo si menciona alguno de estos terminos en el titulo
# o en el extracto. Es una lista amplia a proposito: mejor dejar pasar algo de
# ruido que perder una senal. Agregar terminos aqui cuando algo se escape.
TEMAS = (
    "artificial intelligence", "ai", "genai", "generative", "machine learning",
    "algorithm", "algorithmic", "automation", "automated", "chatbot", "llm",
    "large language model", "data protection", "privacy", "innovation",
    "startup", "startups", "entrepreneur", "entrepreneurship", "sme", "smes",
    "small business", "digital transformation", "productivity", "robot",
    "robotics", "semiconductor", "chips", "regulation", "governance",
    "inteligencia artificial", "inteligencia", "algoritmo", "algoritmos",
    "innovacion", "innovacion", "emprendimiento", "pyme", "pymes",
    "inteligencia artificial", "inovacao", "inovação", "inteligência artificial",
    "algoritmo", "empreendedorismo", "regulacao", "regulação",
    "deepfake", "deepfakes", "synthetic media", "facial recognition",
    "surveillance", "copyright", "openai", "anthropic", "nvidia",
    "modelo de linguagem", "aprendizaje automatico", "datos personales",
    "dados pessoais", "reconhecimento facial",
)

ATOM = "{http://www.w3.org/2005/Atom}"


def leer_medios(ruta):
    """Lector minimo: lineas 'nombre: url' bajo la clave medios."""
    medios = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        limpia = linea.strip()
        if not limpia or limpia.startswith("#") or limpia == "medios:":
            continue
        if limpia.startswith("- "):
            limpia = limpia[2:]
        if ": " in limpia:
            nombre, url = limpia.split(": ", 1)
            url = url.strip().strip('"').strip("'")
            nombre = nombre.strip()
            nivel = "prensa"
            if "[" in nombre and "]" in nombre:
                nivel = nombre[nombre.index("[") + 1:nombre.index("]")].strip()
                nombre = nombre[:nombre.index("[")].strip()
            if url.startswith("http"):
                medios.append((nombre, url, nivel))
    return medios


def pedir(url):
    cabeceras = {
        "User-Agent": AGENTE,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
    }
    solicitud = urllib.request.Request(url, headers=cabeceras)
    with urllib.request.urlopen(solicitud, timeout=30) as respuesta:
        return respuesta.read()


# En las fuentes de nivel "practica" todo menciona IA, asi que ese filtro no
# discrimina: se exige ademas una palabra de negocio o aplicacion. Sin esto la
# bandeja se llena de tutoriales tecnicos.
# Raices, no palabras completas: "govern" cubre governance y governed.
TEMAS_NEGOCIO = (
    "business", "compan", "firm", "enterpris", "sme", "startup",
    "manager", "managem", "executive", "board", "strateg", "productiv",
    "adopt", "roi", "customer", "market", "industr", "polic", "regulat",
    "govern", "workforce", "job", "labor", "labour", "opinion", "econom",
    "invest", "empresa", "pyme", "negocio", "gesti", "estrategia",
    "mercado", "empresarial", "trabalh", "polít", "polit",
)


def es_del_tema(titulo, extracto, nivel="prensa"):
    texto = f"{titulo} {extracto}".lower()
    if not any(re.search(rf"\b{re.escape(t)}\b", texto) for t in TEMAS):
        return False
    if nivel == "practica":
        return any(re.search(rf"\b{re.escape(t)}\w*", texto) for t in TEMAS_NEGOCIO)
    return True


def limpiar(texto):
    sin_etiquetas = re.sub(r"<[^>]+>", " ", texto or "")
    return re.sub(r"\s+", " ", sin_etiquetas).strip()


def parsear(xml_bytes, medio, nivel="prensa", url_feed=""):
    """Acepta RSS 2.0 y Atom, que son los dos formatos en circulacion."""
    try:
        arbol = ET.fromstring(xml_bytes)
    except ET.ParseError:
        inicio = xml_bytes[:400].decode("utf-8", "ignore").lower()
        if "<html" in inicio or "<!doctype html" in inicio:
            raise RuntimeError("la URL responde HTML, no es un feed RSS/Atom") from None
        raise
    entradas = arbol.findall(".//item") or arbol.findall(f".//{ATOM}entry")

    # Base para completar enlaces relativos: el feed declara la direccion del
    # sitio en el canal. El dominio del feed no sirve: HBR lo publica desde
    # feeds.harvardbusiness.org pero los articulos viven en hbr.org.
    base = ""
    canal = arbol.find("channel")
    if canal is not None:
        base = (canal.findtext("link") or "").strip()
    if not base:
        etiqueta = arbol.find(f"{ATOM}link")
        if etiqueta is not None:
            base = etiqueta.get("href", "")
    base = base or url_feed
    resultados = []

    for entrada in entradas[:MAX_POR_MEDIO]:
        titulo = entrada.findtext("title") or entrada.findtext(f"{ATOM}title") or ""

        enlace = entrada.findtext("link") or ""
        if not enlace:
            etiqueta = entrada.find(f"{ATOM}link")
            enlace = etiqueta.get("href", "") if etiqueta is not None else ""
        enlace = enlace.strip()
        # Algunos feeds, como el de HBR, entregan rutas relativas sin dominio.
        if enlace and not enlace.startswith("http") and base:
            enlace = urllib.parse.urljoin(base, enlace)

        fecha = (
            entrada.findtext("pubDate")
            or entrada.findtext(f"{ATOM}published")
            or entrada.findtext(f"{ATOM}updated")
            or ""
        )

        # Extracto corto: senal para decidir si vale la pena leer, no contenido a publicar.
        extracto = (
            entrada.findtext("description")
            or entrada.findtext(f"{ATOM}summary")
            or ""
        )

        titulo_limpio = limpiar(titulo)
        extracto_limpio = limpiar(extracto)[:200]
        if not es_del_tema(titulo_limpio, extracto_limpio, nivel):
            continue

        resultados.append({
            "fuente": "rss",
            "medio": medio,
            "nivel": nivel,
            "titulo": titulo_limpio,
            "enlace": enlace,
            "fecha": fecha.strip(),
            "extracto": extracto_limpio,
        })

    return resultados


def main():
    BANDEJA.mkdir(parents=True, exist_ok=True)
    hallazgos = []

    for medio, url, nivel in leer_medios(MEDIOS):
        try:
            nuevos = parsear(pedir(url), medio, nivel, url)
            hallazgos.extend(nuevos)
            aviso = "  <-- no aporto titulares: revisar el feed" if not nuevos else ""
            print(f"{medio}: {len(nuevos)}{aviso}")
        except Exception as error:
            print(f"  aviso: fallo {medio}: {error} | URL: {url}")

    salida = BANDEJA / f"{date.today().isoformat()}-medios.json"
    salida.write_text(json.dumps(hallazgos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(hallazgos)} titulares -> {salida.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
