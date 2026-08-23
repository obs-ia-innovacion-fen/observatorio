---
name: ficha-de-paper
description: Convierte un artículo académico en una ficha publicable del Observatorio, con resumen en lenguaje llano, evaluación metodológica y una sección de implicancias para empresas y directorios en Chile y la región. Úsala al procesar cualquier paper de la bandeja de fuentes o entregado directamente.
---

# Ficha de paper

## Regla de verificacion: la mas importante

La bandeja solo trae titulo, autores, revista y DOI. NO trae el resumen.
Por lo tanto, ninguna cifra, metodo, muestra, pais o resultado puede escribirse
si no proviene de una fuente que se leyo de verdad.

Antes de escribir hay que abrir el articulo o al menos su resumen. En el
frontmatter se declara que se consulto, con el campo `fuente_ficha`:
`texto completo`, `resumen` o `solo metadatos`.

Si solo hay metadatos, la ficha no se escribe. Se deja el registro como
sugerencia de lectura de una linea y se pasa al siguiente.

Nunca inventar ni estimar una muestra, un pais o un porcentaje. Un dato preciso
y falso hace mas dano que no publicar nada.

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

1. **En una frase** — qué se estudió y qué se encontró. Maximo 40 palabras, en dos
   oraciones si hace falta. Sin siglas, sin nombres de marcos teoricos, sin palabras
   como "mediadora" o "constructo". Es la linea que lee alguien que no es academico:
   si no se entiende en voz alta, esta mal escrita. El marco teorico va en la
   seccion siguiente, no aqui.
2. **Cómo se hizo** — datos, método, período, tamaño de muestra. Suficiente para que el
   lector calibre cuánto peso darle al resultado.
3. **Qué implica** — sección obligatoria. La cobertura del Observatorio es global; el
   lente de lectura es regional. Para trabajos aplicados, el marco de referencia es el
   Cono Sur: Chile, Brasil y Argentina.

   Excepcion: en el area de frontera del conocimiento, donde el trabajo puede no tener
   todavia lectura regional evidente, la seccion responde otra pregunta —que tendria que
   ser cierto para que esto llegue a una empresa de menor tamano, y cuanto falta para
   eso— y no se fuerza una mencion a los tres paises. Forzarla produce parrafos vacios.

   Para todo lo demas: Qué significa el hallazgo para una empresa, un
   directorio o un emprendedor de esos tres paises. Los tres se nombran
   explicitamente y no se sustituyen por "America Latina" ni se reemplazan por
   otros paises de la region. Considerar sus diferencias de
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

Tampoco afirmar que un resultado "es consistente con la evidencia comparada" o
"coincide con la literatura" sin citar al menos un trabajo concreto. Sin cita,
esa frase se elimina.
La credibilidad del Observatorio depende más de lo que se matiza que de lo que se afirma.

## Qué nunca hacer

- Publicar sin la sección "Qué implica".
- Presentar un hallazgo preliminar como establecido.
- Omitir el conflicto de interés cuando el autor pertenece al Observatorio: se declara.
- Aplicar un estándar más laxo a los artículos propios que a las sugerencias.
