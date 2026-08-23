---
name: extraer-indicadores
description: Extrae cifras de informes largos (AI Index, ILIA, encuestas nacionales de innovación) hacia datos/indicadores.yml, dejando el rastro necesario para que una persona las verifique. Úsala cuando salga una edición nueva de un informe de referencia.
---

# Extraer indicadores

Esta skill llena `datos/indicadores.yml` a partir de un informe. No publica
nada: deja candidatos listos para que alguien los confirme.

## La regla que ordena todo

Ninguna cifra se escribe sin el número de página o de figura donde aparece.
Sin esa referencia, verificarla obliga a releer el informe completo, y en la
práctica nadie lo hace: la cifra queda publicada sin revisar.

Toda cifra extraída entra con `verificado:` vacío. Ese campo lo llena una
persona después de comprobarla, no el proceso automático.

## Qué extraer

Solo cifras que sirvan a alguna de las áreas declaradas en `contenido/areas/`.
Un informe de referencia trae cientos de datos y casi todos son irrelevantes
para este Observatorio.

Prioridad, en orden:

1. Cifras de Chile, Brasil o Argentina, individualmente.
2. Cifras de América Latina como región, cuando permitan situar a los tres.
3. Cifras globales que sirvan de referencia para contrastar.
4. Series temporales comparables entre países, que van en el bloque `series`.

Se descartan: cifras sobre países sin relación con la región, comparaciones
que el propio informe advierte como no comparables entre ediciones, y
proyecciones a futuro.

## Cómo se escribe cada una

Campos obligatorios: `clave`, `titulo` (la cifra), `detalle` (qué significa, en
una línea y en palabras propias), `ambito`, `fuente`, `anio`, `enlace`,
`pagina`. El campo `verificado` queda vacío.

El `detalle` es redacción propia, no copia de la leyenda del informe. Las
cifras son hechos y se citan; el texto que las acompaña es obra del autor.

Nunca reproducir los gráficos del informe. Si la serie sirve, se cargan los
datos en el bloque `series` y el sitio dibuja su propio gráfico, citando la
fuente.

## Advertencias metodológicas

Los índices compuestos suelen cambiar de metodología entre ediciones. Si el
informe lo advierte, la advertencia va en el campo `nota` de la serie. Comparar
un puntaje de 2024 con uno de 2026 sin esa nota produce una afirmación falsa.

Cuando una cifra dependa de una definición discutible —qué cuenta como empresa
que adopta IA, por ejemplo— decirlo en el `detalle`.

## Qué reportar al terminar

Cuántas cifras se extrajeron, cuáles quedaron pendientes de verificación, y qué
se descartó por no calzar con ninguna área. Si el informe trae algo que sugiere
un área nueva, mencionarlo: es una decisión editorial, no automática.
