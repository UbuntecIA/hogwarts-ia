# Formatos de entrega

Todo pedido entrega **siempre** un `RESUMEN.md` (en la carpeta del pedido) y las **salidas
finales en `salidas/<tema>/`** (en la raíz del proyecto). Según lo que la persona marque en el
briefing, también: **PPT**, **Word**, **JSON para otra IA** y **prompts de imágenes**.

## 0. Marcadores (los únicos permitidos en una salida)
- `[COMPLETAR: qué dato va aquí]` → datos propios de ITERHUB o del cliente que la persona llena a
  mano: precio, fecha, nombre del programa, enlace, cifra interna, logo del cliente. Van
  visibles también en la PPT y en el Word. El RESUMEN lista todos los que quedaron.
- `[DATO NO ENCONTRADO: qué se buscó, dónde]` → información pública que se buscó y no apareció.
- Nada más: ni `SUPUESTO`, ni `BORRADOR`, ni `VERIFICAR`, ni notas internas. Lo que no está
  listo se dice en el RESUMEN, no dentro de la pieza.

## 1. RESUMEN.md (lo escribe Dumbledore al final)
```markdown
# <Nombre del pedido>
**Fecha:** AAAA-MM-DD · **Nivel:** Profesional · **Modelo:** sonnet · **Fuentes verificadas:** 14 · **Equipo:** Lupin, Hermione, Sprout, McGonagall

## Lo que pediste
<Objetivo, público y entregable principal, tal como quedaron en el briefing, con tus respuestas>

## Resumen
<5 a 8 líneas: qué se hizo, cómo está organizado el entregable y las decisiones clave>

## Lo que te entregamos
| Archivo | Qué es | Para qué lo usas |
|---|---|---|
| salidas/curso-definicion-mercado/00_entrega_completa.md | Todo integrado, revisado por Dumbledore | Leerlo de principio a fin |
| salidas/curso-definicion-mercado/presentacion.pptx | PPT de 32 diapositivas con notas del docente | Dictar la clase |
| salidas/curso-definicion-mercado/investigacion.md | Marcos, 5 casos reales y bibliografía APA | Preparar la clase y responder preguntas |

## Cómo trabajó el equipo
- Oleada 1 (en paralelo): Hermione (investigación), Lupin (estructura)
- Oleada 2 (en cascada): Lupin (contenido de cada diapositiva)
- Oleada 3 (en cascada): Sprout (PPT y Word)
- Revisión: McGonagall · Cierre e integración: Dumbledore

## Revisión de calidad
<Veredicto de McGonagall sobre el cumplimiento del pedido y la calidad, qué se corrigió y qué ajustó Dumbledore>

## Datos que debes completar
<Lista exacta de los [COMPLETAR: …] que quedaron y en qué archivo y diapositiva están>

## Imágenes por generar
<N imágenes. Los prompts están en salidas/<tema>/prompts_imagenes.md con el nombre de archivo de cada una. Guárdalas en salidas/<tema>/imagenes/ y ejecuta `python3 herramientas/crear_pptx.py salidas/<tema>/presentacion.json salidas/<tema>/presentacion.pptx`, o dime "ya puse las imágenes" y lo hago yo. Mientras tanto, la PPT muestra una ilustración de marca en su lugar.>

## Pendientes
<Lo que no se encontró ([DATO NO ENCONTRADO]), lo que no cumple del todo y por qué, lo que debe aprobar una persona>

## Siguientes pasos sugeridos
<2 o 3 acciones concretas>
```

## 2. Salidas: `salidas/<tema>/`
```
ITERHUB Oficina de Agentes/
├── pedidos/2026-11-02_curso-definicion-mercado/   ← instrucciones y trabajo: ORDEN, borradores, revisión, RESUMEN
└── salidas/curso-definicion-mercado/              ← solo lo final que pediste
    ├── 00_entrega_completa.md                     ← todo integrado y revisado (herramientas/integrar.py)
    ├── PARA_OTROS_AGENTES.md                      ← traspaso: qué es cada archivo, qué cambiar y qué no, cómo regenerar
    ├── manifiesto.json                            ← inventario de archivos para que lo lea un agente
    ├── presentacion.pptx                          ← el material para dictar
    ├── presentacion.json                          ← el guion de la PPT (se puede editar y regenerar)
    ├── prompts_imagenes.md                        ← si la PPT tiene imágenes: un prompt por imagen, con su nombre de archivo
    ├── imagenes/                                  ← aquí guardas las imágenes que generes; al regenerar la PPT quedan insertadas
    ├── investigacion.md                           ← casos reales, marcos y bibliografía
    ├── taller.md / taller.docx                    ← si se pidió
    └── fuentes.md                                 ← Profesional y Experto
```
- `<tema>` es un nombre corto en minúsculas con guiones. Si ya existe, se reutiliza. Si el
  nombre de un archivo ya existe, se agrega la fecha (`_2026-11-02`).
- Solo versiones finales, limpias, con nombres claros. Borradores, ORDEN, revisiones y notas se
  quedan en `pedidos/`.

## 3. Presentación PPT (`herramientas/crear_pptx.py`)
La escribe **quien domina el contenido** (Lupin en Academia, Harry o quien hizo el documento en
Marketing) como `presentacion.json`; el productor (Sprout o Dean) la genera, la revisa y
mejora el diseño **sin recortar contenido**:
```
python3 herramientas/crear_pptx.py <ruta>/presentacion.json <ruta>/presentacion.pptx
```
Reglas de una PPT profesional (skill `presentacion-profesional`): una idea por diapositiva pero
**con contenido real** (definición, pasos, dato con fuente, caso, pregunta), nunca viñetas de
una palabra; **notas** en prosa de 80 a 200 palabras con lo que se dice; toda cifra con su
`fuente`; `[COMPLETAR: …]` donde falte un dato propio.

Esquema:
```json
{
  "titulo": "Definición de mercado para emprendimientos de TI",
  "subtitulo": "Sesión de 2 horas · Maestría en [COMPLETAR: nombre del programa]",
  "formato": "16:9",
  "diapositivas": [
    {"tipo": "portada", "titulo": "…", "subtitulo": "…", "notas": "…"},
    {"tipo": "agenda", "titulo": "Qué veremos hoy", "bloques": [{"titulo": "Mercado, segmento y nicho", "tiempo": "25 min"}, {"titulo": "…", "tiempo": "…"}], "notas": "…"},
    {"tipo": "seccion", "titulo": "Bloque 1 · …", "subtitulo": "25 min", "notas": "…"},
    {"tipo": "contenido", "titulo": "…", "texto": "Párrafo de 1 a 3 frases que explica la idea.", "puntos": ["punto desarrollado", {"t": "punto con detalle", "sub": ["detalle 1", "detalle 2"]}], "fuente": "Autor (año)", "notas": "…"},
    {"tipo": "definicion", "termino": "Segmento", "definicion": "…", "ejemplo": "…", "fuente": "…", "notas": "…"},
    {"tipo": "pasos", "titulo": "Cómo estimar el SOM", "pasos": [{"titulo": "Cuenta los clientes del segmento", "texto": "…"}, {"titulo": "…", "texto": "…"}], "notas": "…"},
    {"tipo": "caso", "empresa": "Truora (Colombia)", "contexto": "…", "accion": "…", "resultado": "…", "leccion": "…", "fuente": "Forbes Colombia, 2024", "notas": "…"},
    {"tipo": "cifras", "titulo": "…", "cifras": [{"valor": "43 %", "texto": "de las startups… (CB Insights, 2025)"}], "notas": "…"},
    {"tipo": "tabla", "titulo": "TAM, SAM y SOM", "columnas": ["Concepto", "Qué mide", "Cómo se calcula"], "filas": [["TAM", "…", "…"], ["SAM", "…", "…"]], "fuente": "…", "notas": "…"},
    {"tipo": "dos_columnas", "titulo": "…", "izquierda": {"titulo": "Antes", "puntos": ["…"]}, "derecha": {"titulo": "Después", "puntos": ["…"]}, "notas": "…"},
    {"tipo": "pregunta", "texto": "¿Quién es el cliente que más sufre el problema que resuelves?", "pistas": ["Piensa en quien ya paga por una solución parcial"], "notas": "…"},
    {"tipo": "actividad", "titulo": "Ejercicio: tu frase de mercado", "instrucciones": ["…", "…"], "tiempo": "10 min", "entregable": "Una frase con quién, problema, resultado y alternativa actual", "notas": "…"},
    {"tipo": "cita", "texto": "…", "autor": "Steve Blank, The Four Steps to the Epiphany (2005)", "notas": "…"},
    {"tipo": "diagrama", "subtipo": "circulos", "titulo": "TAM, SAM y SOM", "items": [{"titulo": "TAM", "texto": "…"}, {"titulo": "SAM", "texto": "…"}, {"titulo": "SOM", "texto": "…"}], "fuente": "…", "notas": "…"},
    {"tipo": "diagrama", "subtipo": "proceso", "titulo": "…", "items": [{"titulo": "Paso", "texto": "…"}], "notas": "…"},
    {"tipo": "grafico", "subtipo": "columnas", "titulo": "…", "series": [{"etiqueta": "2023", "valor": 1301, "texto": "1.301"}], "fuente": "…", "notas": "…"},
    {"tipo": "iconos", "titulo": "…", "items": [{"icono": "🔥", "titulo": "Dolor", "texto": "…"}], "notas": "…"},
    {"tipo": "linea_tiempo", "titulo": "…", "hitos": [{"fecha": "2018", "texto": "…"}], "fuente": "…", "notas": "…"},
    {"tipo": "imagen", "titulo": "…", "archivo": "tendero.png", "descripcion": "Qué debe mostrar la imagen (la genera la persona con su IA; prompt en prompts_imagenes.md)", "texto": "Texto opcional al lado", "pie": "…", "notas": "…"},
    {"tipo": "cierre", "titulo": "Lo que te llevas", "subtitulo": "…", "notas": "…"}
  ]
}
```
`formato`: `16:9` (presentación), `4:5` (carrusel), `1:1` o `9:16` (historias). Todos los tipos
aceptan `notas` y `fuente`. `diagrama` admite `subtipo` `circulos`, `embudo`, `proceso`, `ciclo`
y `piramide`; `grafico`, `barras` o `columnas`. `portada` y `contenido` aceptan `"imagen":
"archivo.png"`. Las imágenes se buscan en `imagenes/` junto al JSON: si el archivo no existe,
la diapositiva muestra una ilustración de marca con la descripción, y `crear_pptx.py` avisa
cuáles faltan. Regla de diseño: al menos una de cada tres diapositivas es visual (skill
`presentacion-profesional`, sección 4b).

## 4. Documento Word (`herramientas/crear_docx.py`)
Se escribe primero en Markdown (el mismo archivo que va a salidas) y se convierte:
```
python3 herramientas/crear_docx.py <ruta>/documento.md <ruta>/documento.docx --titulo "…" --subtitulo "…"
```
Soporta títulos (`#`, `##`, `###`), párrafos, viñetas, listas numeradas, tablas, negrita,
cursiva, citas (`>`) y saltos de página (`---` solo en una línea). Lleva portada con la marca
ITERHUB, encabezado y pie con número de página. Skill `documento-word`.

## 5. JSON para construirlo en otra IA (`para_otra_ia.json`)
Para que la persona lo pegue en Gamma, Canva, Beautiful.ai, ChatGPT o similares:
```json
{
  "proyecto": "…", "marca": {"nombre": "ITERHUB", "colores": {"azul": "#002F6C", "amarillo": "#FFCC00"}, "tipografias": ["Poppins", "Inter"], "tono": "…"},
  "publico": "…", "objetivo": "…",
  "secciones": [{"titulo": "…", "contenido": "texto completo…", "elementos_visuales": "…", "notas": "…"}],
  "instrucciones_para_la_ia": "Construye … respetando los textos tal cual; no inventes datos; donde diga [COMPLETAR] deja el espacio."
}
```

## 6. Prompts de imágenes (`prompts_imagenes.md` y `prompts_imagenes.json`)
Los escribe **Tonks** (directora de arte) para toda PPT, en `salidas/<tema>/`. Las imágenes
las generan **siempre los agentes de ChatGPT de la persona**, después de la entrega (nunca se
pregunta quién ni con qué IA), y las guardan en `salidas/<tema>/imagenes/` con el nombre
indicado. Formato exacto: ver el agente `direccion-arte`. Cada prompt trae, en este orden:
tamaño ("imagen horizontal para una diapositiva de PowerPoint, 16:9, 1920 × 1080"), objetivo de
la imagen en esa diapositiva, tipo de imagen, escena y elementos concretos con encuadre, fondo
(y si deja espacio para texto), luz y paleta (azul #002F6C y amarillo #FFCC00 como acentos), y
lo que no debe tener (texto dentro de la imagen, logos, marcas ajenas, personas reales
identificables, cifras). Entre 80 y 160 palabras, en lenguaje natural claro para ChatGPT, con la
proporción en palabras (sin parámetros de otras herramientas).
- **Mínimo una de cada tres diapositivas** lleva imagen (15 → 5; 32 → 11), nunca dos seguidas.
- Al final del `.md` y en el `.json`, la instrucción para regenerar la PPT:
  `python3 herramientas/crear_pptx.py salidas/<tema>/presentacion.json salidas/<tema>/presentacion.pptx`.

## 7. Traspaso a otros agentes (`PARA_OTROS_AGENTES.md`)
Lo escribe Hagrid (`guardabosques`) en toda entrega, por encargo de Dumbledore (o el
propio Dumbledore si no lo llama). Después de ITERHUB, el trabajo lo toman otros agentes de IA
que generan las imágenes y mejoran o rehacen lo que haga falta; este archivo es lo primero que
leen. Rutas completas desde la raíz del proyecto (la carpeta donde está
CLAUDE.md en el computador de la persona; en el archivo se escriben relativas, `salidas/<tema>/…`, y se indica
la raíz una vez). El archivo es profesional: sin nombres de personajes ni referencias a
Hogwarts; el autor se firma como ITERHUB.
```markdown
# Para otros agentes · <Título del pedido>
Raíz del proyecto: <ruta absoluta de la carpeta del proyecto en este computador>
Carpeta de esta entrega: salidas/<tema>/
Fecha: AAAA-MM-DD · Nivel: Profesional · Hecho por: equipo de agentes de ITERHUB (Claude Code)

## Objetivo y público (no cambiar)
<Objetivo y público textuales de la ORDEN>

## Qué hay en la carpeta
| Archivo | Qué es | Fuente editable | Qué pueden hacer |
|---|---|---|---|
| presentacion.pptx | La PPT para dictar (33 diapositivas, con notas) | presentacion.json | Mejorar diseño, insertar imágenes; o rehacerla desde el JSON |
| presentacion.json | Guion completo de la PPT, diapositiva por diapositiva | — | Es la fuente de verdad del contenido |
| prompts_imagenes.json / .md | Imágenes por generar, una por diapositiva, con prompt y nombre de archivo | — | Generar cada imagen y guardarla en imagenes/ |
| imagenes/ | Carpeta de las imágenes (vacía al entregar) | — | Guardar aquí con el nombre exacto |
| investigacion.md | Marcos, casos reales y bibliografía | — | Consultar; no cambiar hechos |
| fuentes.md | Registro de fuentes verificadas | — | Consultar |
| 00_entrega_completa.md | Todo integrado | — | Leer de corrido |

## Qué NO cambiar
- Hechos, cifras, casos y citas: todos tienen fuente en fuentes.md; no se inventan ni se "mejoran".
- Los marcadores [COMPLETAR: …]: los llena la persona; no se rellenan con supuestos.
- Público, objetivo y tono: son los que pidió la persona.
- Marca ITERHUB: azul #002F6C, amarillo #FFCC00, Poppins e Inter, logos de oficina3d/marca/.

## Qué se espera de ustedes
1. Generar las imágenes de prompts_imagenes.json con el nombre exacto y guardarlas en imagenes/.
2. Regenerar la PPT: `python3 herramientas/crear_pptx.py salidas/<tema>/presentacion.json salidas/<tema>/presentacion.pptx` (desde la raíz del proyecto), o insertar cada imagen en su diapositiva conservando título, texto y notas.
3. Mejorar el diseño si lo consideran, partiendo de presentacion.json (pueden cambiar tipos de diapositiva y distribución; no el contenido).
4. Si rehacen un documento, partir del .md correspondiente y conservar las citas.

## Pendientes conocidos
<[DATO NO ENCONTRADO: …] y lo que quedó sin resolver, para que no lo "arreglen" inventando>
```
`manifiesto.json` lo genera `herramientas/integrar.py`: lista cada archivo con su ruta relativa,
tipo, tamaño y, si es la PPT, el número de diapositivas y las imágenes pendientes.
