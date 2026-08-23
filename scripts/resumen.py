"""
Resumen legible de la bandeja de recoleccion.

Convierte los JSON del dia en un unico archivo Markdown ordenado por area y por
fuente, para hacer el triaje editorial sin abrir los JSON uno por uno.

Uso:  python scripts/resumen.py            (usa la fecha de hoy)
      python scripts/resumen.py 2026-08-22 (una fecha especifica)
"""

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BANDEJA = RAIZ / "fuentes" / "bandeja"


def cargar(fecha):
    archivos = sorted(BANDEJA.glob(f"{fecha}-*.json"))
    return [(a, json.loads(a.read_text(encoding="utf-8"))) for a in archivos]


def etiqueta_area(archivo, fecha):
    return archivo.stem.replace(f"{fecha}-", "")


def main():
    fecha = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    archivos = cargar(fecha)

    if not archivos:
        print(f"No hay archivos de bandeja para {fecha}")
        return

    lineas = [f"# Bandeja del {fecha}", ""]
    total = 0

    for archivo, registros in archivos:
        area = etiqueta_area(archivo, fecha)
        por_fuente = Counter(r.get("fuente", "?") for r in registros)
        detalle = ", ".join(f"{k}: {v}" for k, v in sorted(por_fuente.items()))
        lineas += [f"## {area}", f"{len(registros)} registros ({detalle})", ""]
        total += len(registros)

        revistas = Counter(r.get("revista", "") for r in registros if r.get("revista"))
        if revistas:
            top = ", ".join(f"{nombre} ({n})" for nombre, n in revistas.most_common(5))
            lineas += [f"Revistas mas frecuentes: {top}", ""]

        for fuente in sorted(por_fuente):
            lineas.append(f"### {fuente}")
            for r in registros:
                if r.get("fuente") != fuente:
                    continue
                titulo = (r.get("titulo") or "").strip()
                origen = r.get("revista") or r.get("medio") or ""
                sufijo = f" — _{origen}_" if origen else ""
                enlace = r.get("doi") or r.get("enlace") or ""
                lineas.append(f"- [ ] {titulo}{sufijo}  \n      {enlace}")
            lineas.append("")

    lineas.insert(2, f"Total: {total} registros en {len(archivos)} archivos.")
    lineas.insert(3, "")

    salida = BANDEJA / f"{fecha}-resumen.md"
    salida.write_text("\n".join(lineas), encoding="utf-8")
    print(f"{total} registros -> {salida.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
