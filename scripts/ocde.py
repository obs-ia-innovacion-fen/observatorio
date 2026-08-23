"""
Conector con la API de la OCDE (SDMX-JSON).

ESTADO: esqueleto sin verificar. Los identificadores de flujo de datos y las
claves de serie de abajo son una hipotesis: hay que confirmarlos contra la API
real. Por eso existe el modo --descubrir.

No escribe en datos/indicadores.yml. Imprime un bloque YAML listo para pegar,
de modo que una persona revise antes de que algo entre al sitio.

Uso:
    python scripts/ocde.py --descubrir          lista flujos disponibles
    python scripts/ocde.py --probar             prueba una consulta y muestra la URL
    python scripts/ocde.py                      genera el bloque YAML

Nota de cobertura: Chile es miembro de la OCDE, Brasil esta en adhesion y
Argentina no es miembro. Contraintuitivamente, MSTI incluye a Argentina pero
NO a Brasil (verificado 2026-08: 50 economias en MSTI, sin BRA). Para el gasto
en I+D de Brasil hay que ir a PINTEC (IBGE) o al portal RICYT.
Cuando un pais falte, la nota lo declara; no se deja el hueco sin explicar.
"""

import json
import sys
import urllib.error
import urllib.request

BASE = "https://sdmx.oecd.org/public/rest"
AGENTE = "ObservatorioFEN/1.0 (jeosepulve@fen.uchile.cl)"

# ISO3 de los tres paises del alcance.
PAISES = {"CHL": "Chile", "BRA": "Brasil", "ARG": "Argentina"}

# Flujo MSTI: OECD.STI.STP / DF_MSTI / v1.3 (verificado via --descubrir).
# DSD_MSTI declara 6 dimensiones en este orden:
#   REF_AREA . FREQ . MEASURE . UNIT_MEASURE . PRICE_BASE . TRANSFORMATION
# El filtro va con puntos separadores; un slot vacio significa "todos los codigos".
#
# Codigos usados abajo (de CL_MEASURE / CL_UNIT_MEASURE / CL_FREQ / CL_PRICES / CL_TRANSFORMATION):
#   G          Gross Domestic Expenditure on R&D (GERD)
#   T_RS       Researchers (headcount)
#   PT_B1GQ    Percentage of GDP
#   PT_EMP     Percentage of employment  (para investigadores/1.000 ocupados usar la unidad correcta)
#   A          Annual
#   _Z         Not applicable  (PRICE_BASE / TRANSFORMATION cuando no aplican)
CONSULTAS = [
    {
        "clave": "gasto-id-pib",
        "titulo": "Gasto en I+D como porcentaje del PIB",
        "unidad": "% del PIB",
        "flujo": "OECD.STI.STP,DSD_MSTI@DF_MSTI,1.3",
        "filtro": "CHL+BRA+ARG.A.G.PT_B1GQ._Z._Z",
        "desde": "2015",
        # MSTI publica solo 50 economias y Brasil no esta entre ellas (verificado
        # 2026-08). Chile tiene lagunas 2018-21, 2023; Argentina cubre 2015-23.
        "nota": "Brasil no forma parte de la base MSTI: la cifra hay que traerla desde PINTEC (IBGE) o RICYT y agregarla a mano.",
    },
]


def pedir(url):
    # El mismo cliente sirve para datos y para metadatos estructurales (descubrir).
    # El servidor de la OCDE elige el content-type segun el endpoint.
    accept = "application/vnd.sdmx.data+json, application/vnd.sdmx.structure+json"
    solicitud = urllib.request.Request(
        url, headers={"User-Agent": AGENTE, "Accept": accept}
    )
    try:
        with urllib.request.urlopen(solicitud, timeout=45) as respuesta:
            return json.loads(respuesta.read())
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP {error.code} | URL: {url}") from None
    except Exception as error:
        raise RuntimeError(f"{error} | URL: {url}") from None


def descubrir():
    """Lista los flujos de datos publicados, para encontrar el identificador real."""
    url = f"{BASE}/dataflow/all/all/latest?format=jsondata"
    print(f"Consultando: {url}\n")
    datos = pedir(url)
    flujos = datos.get("data", {}).get("dataflows", []) or datos.get("dataflows", [])
    for f in flujos:
        nombre = f.get("name", "")
        if any(t in nombre.lower() for t in ("science", "technology", "innovation", "r&d", "ict")):
            print(f"{f.get('agencyID','?')},{f.get('id','?')},{f.get('version','?')}  {nombre}")


def construir_url(consulta):
    return (
        f"{BASE}/data/{consulta['flujo']}/{consulta['filtro']}"
        f"?startPeriod={consulta['desde']}&format=jsondata"
    )


def extraer(datos):
    """SDMX-JSON: los valores vienen indexados por posicion de dimension."""
    estructura = datos.get("data", {}).get("structures", [datos.get("structure", {})])[0]
    dims_serie = estructura.get("dimensions", {}).get("series", [])
    dims_obs = estructura.get("dimensions", {}).get("observation", [])
    if not dims_obs:
        return {}

    anios = [v.get("id") for v in dims_obs[0].get("values", [])]
    pos_pais = next(
        (i for i, d in enumerate(dims_serie) if d.get("id", "").upper() in ("REF_AREA", "LOCATION", "COU")),
        None,
    )
    if pos_pais is None:
        raise RuntimeError("No se encontro la dimension de pais. Revisar la estructura devuelta.")

    codigos = [v.get("id") for v in dims_serie[pos_pais].get("values", [])]
    series = datos.get("data", {}).get("dataSets", [{}])[0].get("series", {})

    resultado = {}
    for llave, contenido in series.items():
        indices = [int(x) for x in llave.split(":")]
        pais = PAISES.get(codigos[indices[pos_pais]])
        if not pais:
            continue
        valores = {}
        for pos, obs in contenido.get("observations", {}).items():
            anio = anios[int(pos)]
            if obs and obs[0] is not None:
                valores[anio] = obs[0]
        if valores:
            resultado[pais] = valores
    return resultado


def a_yaml(consulta, valores):
    faltantes = [p for p in PAISES.values() if p not in valores]
    nota = consulta["nota"]
    if faltantes:
        nota = (nota + " " if nota else "") + f"Sin datos para {', '.join(faltantes)} en esta serie."

    lineas = [
        f"  - clave: {consulta['clave']}",
        f"    titulo: \"{consulta['titulo']}\"",
        f"    unidad: \"{consulta['unidad']}\"",
        '    fuente: "OCDE"',
        '    enlace: "https://data-explorer.oecd.org"',
        "    verificado:",
        f"    nota: \"{nota.strip()}\"" if nota.strip() else '    nota: ""',
        "    paises:",
    ]
    for pais, serie in valores.items():
        pares = ", ".join(f"{a}: {v}" for a, v in sorted(serie.items()))
        lineas.append(f"      {pais}: {{ {pares} }}")
    return "\n".join(lineas)


def main():
    if "--descubrir" in sys.argv:
        descubrir()
        return

    bloques = []
    for consulta in CONSULTAS:
        url = construir_url(consulta)
        if "--probar" in sys.argv:
            print(f"\n{consulta['clave']}\n  {url}")
        try:
            valores = extraer(pedir(url))
        except Exception as error:
            print(f"  fallo {consulta['clave']}: {error}")
            continue
        if not valores:
            print(f"  {consulta['clave']}: la consulta respondio pero sin datos de los tres paises")
            continue
        bloques.append(a_yaml(consulta, valores))
        print(f"  {consulta['clave']}: {len(valores)} paises con datos")

    if bloques:
        print("\n--- pegar bajo 'series:' en datos/indicadores.yml ---\n")
        print("\n\n".join(bloques))
        print("\nDejar 'verificado' en blanco hasta comprobar las cifras en la fuente.")


if __name__ == "__main__":
    main()
