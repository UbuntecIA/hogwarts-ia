---
name: presentacion-profesional
description: Cómo escribir y producir una presentación PPT profesional (de clase, de estrategia o para un cliente) con contenido real en cada diapositiva, notas del presentador, datos con fuente y la marca ITERHUB, usando presentacion.json y herramientas/crear_pptx.py. Úsala siempre que haya que entregar una PPT.
---

# Presentación profesional

Una PPT de ITERHUB se juzga por si **alguien puede dictarla o presentarla con ella y el público
aprende o decide algo**. Esquema del JSON y tipos de diapositiva: `conocimiento/formatos.md`,
sección 3. Marca: `configuracion/marca.md`.

## 1. Quién escribe y quién produce
- La escribe **quien domina el contenido** (Lupin en cursos; Harry o el autor del documento en
  Marketing) como `presentacion.json`.
- La produce **Sprout o Dean**: generan el `.pptx`, lo revisan, ajustan el tipo de
  diapositiva y el diseño, y **no recortan**. Si un texto no cabe, dividen la diapositiva en
  dos; si una lista es larga, la vuelven tabla o pasos.

## 2. Cuántas diapositivas
- Clase: 12–18 por hora (Profesional), 16–22 (Experto).
- Presentación de estrategia o campaña: 15–25 (Profesional), 25–40 (Experto).
- Charla o pitch de 20 min: 12–18.
Menos de eso suele significar que falta contenido; más, que sobra o que hay que dividir en
versión corta y larga.

## 3. Qué lleva cada diapositiva
- **Un título que afirma algo** ("El SOM se calcula de abajo hacia arriba"), no un tema ("SOM").
- **Contenido real:** una definición completa, un proceso con pasos, un dato con fuente, un
  caso con resultado, una comparación, una pregunta para el grupo o un ejercicio. Entre 40 y
  120 palabras visibles. Viñetas de una o dos palabras no son contenido.
- **`notas`:** en prosa, de 80 a 200 palabras: qué se dice, el ejemplo que se cuenta, la
  pregunta que se lanza, la transición. Sin notas no está terminada.
- **`fuente`** cuando hay cifra, cita o caso: autor u organización, año (y medio si aplica).
- **`[COMPLETAR: …]`** visible donde falte un dato propio (nombre del programa, precio, fecha).

## 4. Tipos de diapositiva y cuándo usarlos
| Tipo | Para |
|---|---|
| `portada`, `cierre` | Abrir y cerrar; el cierre dice qué se lleva el público y el siguiente paso |
| `agenda` | Bloques con tiempo (siempre en clases y en presentaciones de más de 15 diapositivas) |
| `seccion` | Abrir cada bloque |
| `contenido` | Idea con párrafo y puntos desarrollados (con `sub` para detalle) |
| `definicion` | Un concepto clave con definición, ejemplo y fuente |
| `pasos` | Procesos y métodos (3 a 6 pasos con texto cada uno) |
| `caso` | Un caso real: empresa, contexto, acción, resultado, lección, fuente |
| `cifras` | 2 a 4 datos fuertes con fuente |
| `tabla` | Comparar conceptos, opciones o escenarios |
| `dos_columnas` | Antes/después, mito/realidad, opción A/B |
| `pregunta` | Pregunta al grupo o al cliente, con pistas |
| `actividad` | Ejercicio con instrucciones, tiempo y entregable |
| `cita` | Una cita real, con autor y obra (menos de 15 palabras si es textual) |
| `diagrama` | Un modelo o proceso visual: `circulos` (TAM/SAM/SOM, capas), `embudo`, `proceso` (3–6 pasos con flechas), `ciclo`, `piramide` |
| `grafico` | Datos reales en `barras` o `columnas` (2–8 valores), siempre con `fuente` |
| `iconos` | 3–4 ideas en tarjetas con ícono (emoji) y texto corto |
| `linea_tiempo` | Historia de un caso o de un plan: 3–6 hitos con fecha |
| `imagen` | Una foto o ilustración que enseña más que el texto (con `archivo`, `descripcion` y, opcional, `texto` al lado) |

Alterna tipos: tres `contenido` seguidas cansan; una clase buena mezcla definición, caso,
pregunta y actividad. Cualquier `contenido` o `portada` acepta `"imagen": "archivo.png"` para
llevar una foto al lado.

## 4b. Diseño visual: la regla de uno de cada tres
Una PPT profesional no es texto con logo. **Al menos una de cada tres diapositivas lleva un
elemento visual** (`diagrama`, `grafico`, `iconos`, `linea_tiempo`, `imagen`, `cifras` o
`caso`), y ninguna sección de más de 4 diapositivas va sin uno. Quien escribe el guion ya
elige el tipo visual pensando en qué enseña más: un proceso → `proceso`; capas o mercado →
`circulos` o `embudo`; cifras en el tiempo → `grafico`; la historia de un caso → `linea_tiempo`;
cuatro criterios → `iconos`; un lugar, una persona, un producto → `imagen`.

**Imágenes (fotos e ilustraciones):** Hogwarts IA no genera imágenes; las generan siempre los
agentes de ChatGPT de la persona, después de la entrega (no se pregunta quién ni con qué IA).
**Tonks (`direccion-arte`)** decide y escribe los prompts; la cadena de toda PPT es guion →
Tonks → producción. El flujo:
1. En el guion, cada `imagen` lleva `"archivo": "nombre.png"` (minúsculas, sin espacios) y
   `"descripcion"` de qué debe mostrar.
2. Tonks escribe `salidas/<tema>/prompts_imagenes.md` y `.json`: un prompt por diapositiva
   (tamaño, objetivo, tipo, escena, fondo, paleta, prohibido) en lenguaje natural para ChatGPT,
   con el nombre de archivo exacto de cada imagen. **Mínimo una de cada tres diapositivas.**
3. Mientras no exista el archivo, la diapositiva muestra una ilustración de marca con la
   descripción, así la PPT ya se ve completa.
4. Los agentes de ChatGPT generan las imágenes y las guardan en `salidas/<tema>/imagenes/` con
   esos nombres; la PPT se regenera con `crear_pptx.py` (o la persona dice "ya puse las
   imágenes") y quedan insertadas.
En una clase de 2 horas, de 3 a 6 imágenes; en una presentación para cliente, portada y 2 a 5
más. Nunca fotos de personas reales identificables ni marcas ajenas.

## 5. Estructuras recomendadas
- **Clase:** portada → agenda → gancho (cifras o pregunta) → por bloque: sección, 2–5 de
  contenido/definición/pasos, un caso, una pregunta o actividad → síntesis (tabla o contenido)
  → aplicación en el trabajo de cada uno (actividad) → cierre → bibliografía (contenido, APA).
- **Estrategia o campaña para cliente/socios:** portada → agenda → resumen ejecutivo → contexto
  y diagnóstico (cifras, tabla de competencia) → público (contenido/dos_columnas) → objetivos
  (cifras) → estrategia y mensajes → plan por canal (tabla) → calendario (tabla) → presupuesto
  (tabla o cifras) → medición (tabla) → riesgos → siguientes pasos → cierre.

## 6. Producción y verificación
```
python3 herramientas/crear_pptx.py <ruta>/presentacion.json <ruta>/presentacion.pptx
```
Antes de entregar, el productor comprueba:
- el archivo se generó sin error y el número de diapositivas coincide con el JSON;
- ninguna diapositiva tiene más texto del que cabe (regla práctica: `contenido` hasta 6
  puntos de una línea y media; `tabla` hasta 6 filas; `pasos` hasta 6);
- todas tienen `notas`; las cifras tienen `fuente`;
- los `[COMPLETAR]` están visibles y listados;
- el amarillo no es texto sobre blanco; los logos son los reales;
- **pase de diseño:** se cumple la regla de uno de cada tres (sección 4b), no hay dos
  diapositivas visuales iguales seguidas, cada `grafico` tiene fuente, y
  `prompts_imagenes.md` existe si hay diapositivas con imagen (con los nombres de archivo).
  El productor puede convertir un `contenido` en `diagrama`, `iconos` o `grafico` **sin
  cambiar el texto**, y anota qué cambió.
Si la persona pidió prompts de imágenes, se escribe un prompt por diapositiva `imagen`
(`conocimiento/formatos.md`, sección 6).
