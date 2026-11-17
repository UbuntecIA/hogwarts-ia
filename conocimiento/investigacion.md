# Protocolo de investigación

ITERHUB es una empresa real: lo que entregamos se presenta a clientes y se dicta en clase, y
tiene que sostenerse con evidencia. Este protocolo aplica a todo agente que investigue, con la
intensidad del nivel (`conocimiento/niveles.md`). La skill `investigacion-profunda` lo lleva
paso a paso.

## 0. Las tres reglas que no se negocian
1. **Nada se inventa.** Ni casos, ni empresas, ni cifras, ni citas, ni testimonios, ni
   "ejemplos ilustrativos". Un caso solo existe si hay una fuente pública que lo cuenta.
2. **Toda fuente se abre.** No se cita de oídas ni "según se sabe". Se abre la página (WebFetch),
   se lee lo que dice, se anota la fecha y se guarda el enlace. Si no carga, se busca otra; no
   se cita lo que no se pudo leer.
3. **Lo que no se encuentra se dice:** `[DATO NO ENCONTRADO: qué se buscó, dónde y cuándo]`.
   Es mejor un hueco honesto que un número bonito.

## 1. Planear antes de buscar
Escribe 3 a 8 preguntas concretas que tu entrega necesita responder. Por ejemplo, para un
curso de definición de mercado para una maestría:
- "¿Qué marcos de referencia usan hoy las escuelas de negocios para definir mercado (Blank,
  Osterwalder, Moore, Christensen) y qué dice la literatura reciente?"
- "¿Qué startups de TI de Colombia o Latinoamérica cambiaron de segmento y lo contaron
  públicamente, con qué resultado?"
- "¿Qué cifras oficiales existen sobre el ecosistema emprendedor TI en Colombia (MinTIC,
  Colombia Fintech, iNNpulsa, DANE) de los últimos 24 meses?"

Busca para responder esas preguntas, no por buscar. Varias búsquedas por pregunta, en español y
en inglés.

## 2. Tipos de fuente (usa primero las de arriba; combina al menos 3 tipos)
1. **Oficiales y primarias:** entidades de gobierno (MinTIC, DANE, SIC, iNNpulsa, DNP), leyes y
   normas, documentación oficial de plataformas (Meta, TikTok, LinkedIn, Google, OpenAI,
   Anthropic), datos abiertos, informes anuales y páginas oficiales de las empresas citadas.
2. **Académicas y de referencia:** artículos revisados por pares, libros de referencia del tema
   (con autor, año y editorial), papers de universidades, arXiv (indica que es preprint),
   Harvard Business Review, MIT Sloan, Stanford AI Index.
3. **Informes de industria:** McKinsey, BCG, Deloitte, Gartner, CB Insights, Statista (solo si
   la fuente original está identificada), We Are Social/Meltwater "Digital", HubSpot, Think
   with Google, LAVCA, Endeavor, Colombia Fintech, Cámara Colombiana de Comercio Electrónico.
4. **Artículos, noticias y revistas:** medios reconocidos de negocios y tecnología (Forbes,
   Bloomberg Línea, La República, Portafolio, El Tiempo, Semana, TechCrunch, Contxto,
   Ecosistema Startup), revistas especializadas, entrevistas publicadas con fundadores.
5. **Observación directa pública:** páginas, precios y temarios de competidores; bibliotecas de
   anuncios (Meta Ad Library, Google Ads Transparency Center); TikTok Creative Center; Google
   Trends; perfiles públicos de referentes.
6. **Débiles (evitar o marcar):** blogs sin autor, contenido generado con IA sin fuentes,
   foros, páginas de "top 10" sin metodología. Si los usas, di por qué y nunca como única
   fuente de una cifra.

## 3. Casos reales
Un caso sirve cuando tiene **empresa real con nombre, contexto, qué hizo, qué pasó (con cifras
si existen) y fuente con fecha**. Escribe cada caso así:
```
**Truora (Colombia, verificación de identidad).** Contexto: … Qué hizo: … Resultado: …
Fuente: <medio o documento>, <fecha>, <enlace>. Lo que enseña para el curso: …
```
- Prioriza Colombia y Latinoamérica; completa con casos globales reconocidos si hacen falta.
- Si solo hay una fuente para un caso, dilo: "fuente única".
- Si la persona pidió un sector o empresas concretas, esos casos son obligatorios; si no se
  encuentran, se marca `[DATO NO ENCONTRADO]` y se explica.

## 4. Reglas de uso
- **Recencia:** tendencias, redes y herramientas de IA: últimos 3 a 6 meses; datos de mercado:
  últimos 12 a 24 meses; marcos teóricos: la edición más reciente del libro o artículo. Si
  algo es más viejo, se dice.
- **Triangula:** toda cifra importante viene de 2 fuentes o de la fuente primaria. Si dos
  fuentes se contradicen, se muestran las dos.
- **Cita siempre**, en el texto y en `fuentes.md`. Formato en el texto: (Autor u organización,
  año). Bibliografía en **APA 7** cuando el entregable es académico (cursos, talleres); en
  Marketing basta nombre, medio, fecha y enlace.
- **No copies textos ajenos:** resume con tus palabras y cita. Nada de reproducir piezas,
  guiones ni textos de otros.
- **Contexto Colombia y Latinoamérica** cuando exista; se dice cuándo un dato es de otro país.

## 5. Registro de fuentes (`CARPETA/fuentes.md`)
Cada agente agrega sus fuentes a este archivo compartido (si no existe, lo crea).
```markdown
| # | Fuente | Tipo | Fecha | Enlace | Qué aporta | Verificada (abierta y leída) | Usada por |
|---|---|---|---|---|---|---|---|
| 1 | MinTIC, Informe … | Oficial | 2026-03 | https://… | Número de empresas TI en Colombia | Sí | Hermione |
```
En Profesional y Experto, `fuentes.md` va también a `salidas/<tema>/`.

## 6. Síntesis (lo que va en tu entrega)
- **Hallazgos:** de 5 a 10, cada uno con su evidencia y su "¿y entonces qué?" para el
  entregable.
- **Marcos de referencia** (cursos): qué propone cada autor, en qué se diferencian, cuándo usar
  cada uno.
- **Casos** (sección 3).
- **Cifras clave** con fuente y fecha, listas para citar en la PPT o el documento.
- **Vacíos:** lo que no se pudo confirmar y qué se buscó.
- **Bibliografía** (APA 7 en Academia).
