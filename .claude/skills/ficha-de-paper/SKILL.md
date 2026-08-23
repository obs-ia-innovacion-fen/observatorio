---
name: ficha-de-paper
description: Convierte un artículo académico en una ficha publicable del Observatorio, con resumen en lenguaje llano, evaluación metodológica y una sección de implicancias para empresas y directorios en Chile y la región. Úsala al procesar cualquier paper de la bandeja de fuentes o entregado directamente.
---

# Ficha de paper

## Antes de escribir

Verifica que el artículo pertenece a un área declarada en `contenido/areas/`. Si no calza
en ninguna, no se procesa: proponer un área nueva es una decisión editorial, no automática.

## Preprints

Si el registro viene marcado con `revisado_por_pares: false` —SSRN, RePEc, NBER, arXiv—
la ficha debe decirlo en la primera linea de "Como se hizo": documento de trabajo,
todavia sin revision por pares. Se pueden publicar, y a veces conviene porque llegan
antes, pero el lector tiene que saber que estatus tiene lo que esta leyendo.

## Reglas de derechos

No reproducir el abstract completo ni fragmentos extensos del artículo. Todo el texto de la
ficha es redacción propia. La única cita textual admisible es una frase breve entrecomillada
cuando la formulación exacta cambia el sentido. Siempre enlazar al DOI original.

## Estructura de salida

Archivo en `contenido/publicaciones/` con el frontmatter completo del esquema y estas
secciones, en este orden:

1. **En una frase** — qué se estudió y qué se encontró. Tres o cuatro líneas, sin jerga.
2. **Cómo se hizo** — datos, método, período, tamaño de muestra. Suficiente para que el
   lector calibre cuánto peso darle al resultado.
3. **Qué implica** — sección obligatoria. El marco de referencia del Observatorio es el
   Cono Sur: Chile, Brasil y Argentina. Qué significa el hallazgo para una empresa, un
   directorio o un emprendedor de esos tres países, considerando sus diferencias de
   tamaño de mercado, madurez digital y marco regulatorio. Cuando el estudio viene de
   otro contexto —y la mayoría vendrá de Asia, Europa o Norteamérica— la pregunta es si
   el resultado se traslada o no, y por qué. Esa evaluación de transferibilidad es el
   aporte propio. Si no es posible escribir esta sección con contenido real, el paper
   no se publica.
4. **Cita** — APA y BibTeX.

## Tono

Registro técnico y sobrio. Sin superlativos, sin "revolucionario", sin "cambia todo".
Cuando la evidencia es débil o el estudio tiene limitaciones relevantes, se dice.
Nunca afirmar que un hallazgo aplica al Cono Sur si el estudio no lo midió ahí: se
plantea como hipótesis a verificar, no como conclusión.
La credibilidad del Observatorio depende más de lo que se matiza que de lo que se afirma.

## Qué nunca hacer

- Publicar sin la sección "Qué implica".
- Presentar un hallazgo preliminar como establecido.
- Omitir el conflicto de interés cuando el autor pertenece al Observatorio: se declara.
- Aplicar un estándar más laxo a los artículos propios que a las sugerencias.
