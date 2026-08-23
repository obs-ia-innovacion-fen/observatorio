# Observatorio de IA e Innovación en los Negocios — sistema de contenidos

Departamento de Administración, Facultad de Economía y Negocios, Universidad de Chile.

Este repositorio contiene el contenido del sitio del Observatorio y el flujo que lo alimenta.
El contenido vive en Markdown, de modo que es independiente de la plataforma de publicación:
si mañana cambia el hosting, el contenido se conserva íntegro.

## Cómo se opera

1. Un script en `scripts/` consulta las fuentes definidas en `fuentes/consultas.yml`
   y deja los resultados sin procesar en `fuentes/bandeja/`.
2. Con las skills de `.claude/skills/` se redactan los borradores a partir de esa bandeja.
3. Los borradores se revisan y se aprueban antes de publicarse. Ninguna pieza se publica
   sin un párrafo de interpretación propia.
4. Al aprobarse, el sitio se reconstruye y la pieza entra en el envío periódico.

## Estructura

```
contenido/
  areas/            una ficha por área temática (define el eje editorial)
  publicaciones/    artículos académicos: propios, de colaboración y sugerencias
  vigilancia/       notas breves sobre hechos recientes, fechadas
  webinars/         cada webinar con su grabación, nota y materiales
fuentes/
  consultas.yml     consultas por área hacia OpenAlex y arXiv
  bandeja/          salida del recolector, material sin procesar
scripts/
  recolectar.py     recolección automática, sin modelo de lenguaje
.claude/skills/     formato de cada tipo de pieza, en formato ejecutable
```

## Convenciones

- El nombre del archivo es la URL para siempre. Minúsculas, sin tildes ni espacios,
  separado por guiones. Las notas de vigilancia llevan fecha al inicio: `2026-08-22-titulo.md`.
- Toda pieza declara su `area`, que debe existir en `contenido/areas/`.
- Nada se publica sin la sección "Qué implica".

## Esquema de metadatos

Campos comunes a toda pieza: `titulo`, `fecha`, `area`, `autor`, `destacado`.

En `publicaciones/`, el campo `tipo` define el tratamiento visual:

| valor          | qué es                                     | cómo se muestra                     |
|----------------|--------------------------------------------|-------------------------------------|
| `propio`       | autoría del Observatorio                   | tarjeta destacada, cita exportable  |
| `colaboracion` | con instituciones socias (FGV, Cambridge)  | tarjeta destacada con institución   |
| `comentada`    | paper ajeno con ficha completa             | tarjeta normal con análisis         |
| `sugerencia`   | lectura recomendada de terceros            | línea simple con enlace al DOI      |


## Continuidad

El repositorio pertenece a la organización del Observatorio, no a una cuenta personal.
Las cuentas de hosting y de envío de correo se asocian a un correo institucional.
Cualquier persona con acceso a la organización puede reconstruir el sitio completo.
