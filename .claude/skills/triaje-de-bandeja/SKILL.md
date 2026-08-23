---
name: triaje-de-bandeja
description: Ordena la bandeja semanal por pertinencia contra las fichas de área y detecta temas que convergen en varios medios. Devuelve una lista corta de candidatos con justificación, sin escribir contenido. Úsala al empezar la sesión semanal, antes de ficha-de-paper o nota-de-vigilancia.
---

# Triaje de bandeja

Cada semana la bandeja trae entre sesenta y cien registros académicos y otros
tantos titulares de prensa. Cinco o seis valen. Esta skill separa esos seis del
resto.

No escribe contenido. Solo selecciona y justifica. La escritura viene después,
con la skill que corresponda al tipo de pieza.

## Qué leer primero

Antes de mirar la bandeja, leer las cuatro fichas de `contenido/areas/`. El
criterio de pertinencia sale de ahí: cada área declara qué entra, qué no entra
y qué preguntas la guían. Un registro es pertinente si ayuda a responder alguna
de esas preguntas, no si trata del mismo tema en general.

También conviene revisar `contenido/publicaciones/` para no proponer algo que
ya se fichó.

## Cómo evaluar cada registro académico

Tres criterios, en este orden:

1. **Pertinencia**: ¿responde a alguna de las preguntas que la ficha de área
   declara? Un paper sobre adopción de IA en pymes de Vietnam puede ser
   pertinente si permite contrastar con el Cono Sur, y no serlo si solo repite
   un hallazgo ya establecido.
2. **Solidez**: revista y editorial. Ante nombres genéricos y editoriales
   desconocidas, desconfiar. Los preprints de repositorios reconocidos son
   aceptables y se marcan como tales.
3. **Aporte propio posible**: ¿se puede escribir una sección de implicancias
   real para Chile, Brasil y Argentina? Si el paper no da pie a eso, no sirve
   por muy bueno que sea.

Un registro que falla el tercer criterio se descarta aunque pase los dos
primeros. Es el filtro que más material elimina y el más importante.

## Cómo evaluar los titulares de prensa

Aquí el trabajo es distinto: no se evalúa registro por registro, se buscan
patrones.

- **Convergencia**: un mismo tema en tres o más medios distintos de la misma
  semana. Reportarlo explícitamente, con los medios que lo cubren. Es el
  disparador principal de una nota de vigilancia.
- **Hechos regulatorios** en Chile, Brasil o Argentina, aunque aparezcan en un
  solo medio.
- **Datos nuevos**: informes con cifras, no opiniones sobre cifras conocidas.

El resto se ignora sin comentario.

## Qué devolver

Un texto breve, en pantalla, no un archivo:

**Candidatos a ficha** — máximo seis, ordenados por pertinencia. Por cada uno:
título, revista, área a la que iría, y una línea diciendo por qué vale. Si es
preprint, decirlo.

**Convergencias detectadas** — cada tema que aparece en tres o más medios, con
los medios que lo cubren y una línea sobre por qué podría importar en la
región.

**Hechos regulatorios** — si los hay, aunque sean de un solo medio.

**Descartes que vale la pena mencionar** — solo si algo parecía prometedor y se
descartó por una razón que conviene que el editor conozca: revista dudosa, tema
ya cubierto, imposibilidad de escribir implicancias.

Nada más. Sin resumir el contenido de los papers, sin adelantar conclusiones,
sin proponer títulos de notas.

## Límites

No inventar el contenido de un registro. La bandeja solo trae metadatos: si
hace falta saber de qué trata un paper más allá del título, se dice que hay que
abrirlo, no se supone.

La decisión final es del editor. Esta skill propone una lista corta; no
determina qué se publica.
