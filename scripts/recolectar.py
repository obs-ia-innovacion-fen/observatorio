"""
Recolector de novedades académicas para el Observatorio.

No usa modelo de lenguaje: solo consulta APIs abiertas y deja el material en
fuentes/bandeja/ para que sea procesado despues con las skills del repositorio.
Sin dependencias externas, de modo que corre tal cual en GitHub Actions.

Uso:  python scripts/recolectar.py
"""

import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONSULTAS = RAIZ / "fuentes" / "consultas.yml"
BANDEJA = RAIZ / "fuentes" / "bandeja"
CONTACTOS = [
    "daviddiazsolis@gmail.com",
    "jeosepulve@fen.uchile.cl",
]
CORREO = CONTACTOS[0]  # OpenAlex acepta un solo mailto
AGENTE = f"Observatorio FEN ({'; '.join(CONTACTOS)})"
MAX_POR_FUENTE = 15


def leer_consultas(ruta):
    """Lector mínimo del YAML propio de este repositorio, sin instalar PyYAML."""
    areas, actual = [], None
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        limpia = linea.strip()
        if limpia.startswith("#") or not limpia:
            continue
        if limpia.startswith("- slug:"):
            actual = {"slug": limpia.split(":", 1)[1].strip()}
            areas.append(actual)
        elif actual and ":" in limpia:
            clave, valor = limpia.split(":", 1)
            valor = valor.strip().strip('"').strip("'").replace('\\"', '"')
            actual[clave.strip()] = int(valor) if valor.isdigit() else valor
    return areas


def pedir(url):
    solicitud = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(solicitud, timeout=30) as respuesta:
        return respuesta.read()


def desde_openalex(consulta, desde_dias):
    if not consulta:
        return []
    corte = (date.today() - timedelta(days=desde_dias)).isoformat()
    parametros = urllib.parse.urlencode({
        "search": consulta,
        "filter": f"from_publication_date:{corte}",
        "per-page": MAX_POR_FUENTE,
        "mailto": CORREO,
    })
    datos = json.loads(pedir(f"https://api.openalex.org/works?{parametros}"))
    return [{
        "fuente": "openalex",
        "titulo": t.get("title") or "",
        "anio": t.get("publication_year"),
        "doi": t.get("doi") or "",
        "autores": [a["author"]["display_name"] for a in t.get("authorships", [])[:6]],
        "citas": t.get("cited_by_count", 0),
    } for t in datos.get("results", [])]


def desde_arxiv(consulta):
    if not consulta:
        return []
    # arXiv rechaza los dos puntos de cat: y abs: cuando van codificados como %3A,
    # asi que la URL se arma a mano en vez de con urlencode.
    codificada = urllib.parse.quote(consulta, safe=':')
    url = (
        "https://export.arxiv.org/api/query"
        f"?search_query={codificada}"
        f"&sortBy=submittedDate&sortOrder=descending&max_results={MAX_POR_FUENTE}"
    )
    try:
        datos = pedir(url)
    except Exception as error:
        raise RuntimeError(f"{error} | URL: {url}") from error
    arbol = ET.fromstring(datos)
    espacio = {"a": "http://www.w3.org/2005/Atom"}
    resultados = []
    for entrada in arbol.findall("a:entry", espacio):
        titulo = (entrada.findtext("a:title", "", espacio) or "").strip()
        resultados.append({
            "fuente": "arxiv",
            "titulo": re.sub(r"\s+", " ", titulo),
            "anio": (entrada.findtext("a:published", "", espacio) or "")[:4],
            "doi": entrada.findtext("a:id", "", espacio),
            "autores": [a.findtext("a:name", "", espacio) for a in entrada.findall("a:author", espacio)[:6]],
            "citas": None,
        })
    return resultados


def main():
    BANDEJA.mkdir(parents=True, exist_ok=True)
    hoy = date.today().isoformat()

    for area in leer_consultas(CONSULTAS):
        slug = area["slug"]
        hallazgos = []
        for obtener in (
            lambda: desde_openalex(area.get("openalex", ""), area.get("desde_dias", 30)),
            lambda: desde_arxiv(area.get("arxiv", "")),
        ):
            try:
                hallazgos.extend(obtener())
            except Exception as error:
                print(f"  aviso: fallo una fuente de {slug}: {error}")

        vistos, unicos = set(), []
        for h in hallazgos:
            clave = (h["titulo"] or "").lower()[:90]
            if clave and clave not in vistos:
                vistos.add(clave)
                unicos.append(h)

        salida = BANDEJA / f"{hoy}-{slug}.json"
        salida.write_text(json.dumps(unicos, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{slug}: {len(unicos)} resultados -> {salida.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()