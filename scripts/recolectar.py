"""
Recolector de novedades académicas para el Observatorio.

No usa modelo de lenguaje: solo consulta APIs abiertas y deja el material en
fuentes/bandeja/ para que sea procesado despues con las skills del repositorio.
Sin dependencias externas, de modo que corre tal cual en GitHub Actions.

Uso:  python scripts/recolectar.py
"""

import json
import os
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
MAX_POR_FUENTE = 12


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


CLAVE_OPENALEX = os.environ.get("OPENALEX_API_KEY", "")

# Fuentes que no son revistas con revision por pares: repositorios y servidores
# de preprints. Se descartan localmente porque OpenAlex no ofrece un filtro de
# calidad editorial documentado.
FUENTES_EXCLUIDAS = (
    "zenodo", "ssrn", "researchgate", "preprints.org", "figshare",
    "open science framework", "research square",
    "zenodo.", "osf.io",
    "authorea", "proceedings", "iconic research", "arxiv",
)

# Repositorios de preprints aceptados: solo entran si el area habilita el tipo
# "preprint" en consultas.yml, y quedan marcados como tales en la salida.
PREPRINTS_ACEPTADOS = (
    "ssrn", "social science research network", "repec", "nber",
)

# Allowlist opcional por editorial. Con EXIGIR_EDITORIAL = True solo pasan las
# editoriales de abajo: mucho mas estricto, pero deja fuera revistas regionales
# legitimas. Agregar aqui las que se decida aceptar caso a caso.
EXIGIR_EDITORIAL = False
EDITORIALES_PERMITIDAS = (
    "elsevier", "springer", "wiley", "taylor & francis", "sage",
    "emerald", "mdpi", "frontiers", "nature", "oxford university press",
    "cambridge university press", "informs", "acm", "ieee",
    "massachusetts institute of technology", "harvard",
)


def reconstruir_resumen(indice):
    """OpenAlex entrega el resumen como indice invertido; se rearma aqui."""
    if not indice:
        return ""
    palabras = [(pos, palabra) for palabra, pos_lista in indice.items() for pos in pos_lista]
    return " ".join(palabra for _, palabra in sorted(palabras))


def esta_excluido(texto, excluye):
    """Cualquier termino de la lista descalifica el registro."""
    if not excluye:
        return False
    texto = texto.lower()
    return any(re.search(rf"\b{re.escape(t.strip().lower())}\b", texto)
               for t in excluye.split("|") if t.strip())


def cumple_requisitos(texto, requiere):
    """requiere: grupos separados por ';', alternativas dentro de cada grupo por '|'.
    Todos los grupos deben aparecer; dentro de un grupo basta una alternativa."""
    if not requiere:
        return True
    texto = texto.lower()
    for grupo in requiere.split(";"):
        alternativas = [a.strip().lower() for a in grupo.split("|") if a.strip()]
        if not any(re.search(rf"\b{re.escape(a)}\b", texto) for a in alternativas):
            return False
    return True


def es_preprint_aceptado(revista):
    return any(x in (revista or "").lower() for x in PREPRINTS_ACEPTADOS)


def es_publicable(revista, editorial=""):
    if not revista:
        return False
    if es_preprint_aceptado(revista):
        return True
    if any(x in revista.lower() for x in FUENTES_EXCLUIDAS):
        return False
    if EXIGIR_EDITORIAL:
        return any(x in (editorial or "").lower() for x in EDITORIALES_PERMITIDAS)
    return True


def desde_openalex(consulta, desde_dias, paises="", requiere="", tipos="article", excluye=""):
    if not consulta:
        return []
    corte = (date.today() - timedelta(days=desde_dias)).isoformat()
    # title_and_abstract.search es mucho mas preciso que search, que tambien
    # revisa el texto completo y por eso trae coincidencias tangenciales.
    filtros = [
        f"title_and_abstract.search:{consulta}",
        f"from_publication_date:{corte}",
        f"type:{tipos or 'article'}",
    ]
    if paises:
        # Filtro duro por afiliacion institucional de los autores. Buscar el
        # nombre del pais en el texto no sirve: la busqueda rankea, no filtra.
        filtros.append(f"authorships.institutions.country_code:{paises}")
    parametros = {
        "filter": ",".join(filtros),
        "sort": "publication_date:desc",
        "per_page": MAX_POR_FUENTE,
        "mailto": CORREO,
    }
    if CLAVE_OPENALEX:
        parametros["api_key"] = CLAVE_OPENALEX
    datos = json.loads(pedir(f"https://api.openalex.org/works?{urllib.parse.urlencode(parametros)}"))

    resultados = []
    for t in datos.get("results", []):
        origen = ((t.get("primary_location") or {}).get("source") or {})
        revista = origen.get("display_name", "")
        editorial = origen.get("host_organization_name", "") or ""
        enlace = t.get("doi") or origen.get("landing_page_url") or t.get("id") or ""
        if not es_publicable(revista, editorial) or not es_publicable(enlace):
            continue
        texto = f"{t.get('title') or ''} {reconstruir_resumen(t.get('abstract_inverted_index'))}"
        if not cumple_requisitos(texto, requiere) or esta_excluido(texto, excluye):
            continue
        resultados.append({
            "fuente": "openalex",
            "tipo": t.get("type", ""),
            "revisado_por_pares": not es_preprint_aceptado(revista),
            "titulo": t.get("title") or "",
            "anio": t.get("publication_year"),
            "doi": enlace,
            "revista": revista,
            "editorial": editorial,
            "autores": [a["author"]["display_name"] for a in t.get("authorships", [])[:6]],
            "citas": t.get("cited_by_count", 0),
        })
    return resultados


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
            lambda: desde_openalex(area.get("openalex", ""), area.get("desde_dias", 30), area.get("paises", ""), area.get("requiere", ""), area.get("tipos", "article"), area.get("excluye", "")),
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
