---
name: curso-y-taller
description: Cómo producir el material profesional de un curso, clase o taller (la PPT completa con notas del docente, la investigación con casos reales y, si se pidió, el taller y el quiz) con el rigor del nivel y del público. Úsala en todo pedido de curso, clase, sesión, charla o taller.
---

# Curso, clase o taller: el material para dictarlo

El entregable principal de un curso es **el material con el que la persona lo dicta**. Lo demás
(sílabos largos, guiones de video, plataformas, "experiencia del estudiante") no se hace salvo
que se haya pedido. Base pedagógica: `conocimiento/academia.md` (secciones 1 a 6). Profundidad:
`conocimiento/niveles.md`. Fuentes: skill `investigacion-profunda`.

## Quién hace qué
- **Hermione** investiga primero: marcos de referencia con autor y año, estado actual del tema,
  casos reales con fuente, cifras clave y bibliografía APA → `investigacion.md`.
- **Lupin** es el dueño del curso: define la estructura por bloques y tiempos y **escribe el
  contenido completo de cada diapositiva** (texto, datos, casos, preguntas, ejercicios) y sus
  notas del docente → `presentacion.json`. Mientras Hermione investiga, Lupin adelanta la
  estructura; el contenido de fondo lo escribe con la investigación en la mano.
- **Sprout** produce: genera la PPT con `crear_pptx.py`, revisa que abra y que nada se
  desborde, mejora el tipo de diapositiva cuando conviene (tabla, caso, pasos), produce el Word
  si se pidió y las plantillas del taller. **No recorta ni resume**: si no cabe, divide.
- **Flitwick** (solo si se pidió taller, ejercicios o quiz): diseña el taller completo o el quiz,
  alineados con los bloques de Lupin.
- **Cho** (solo si se pidió): documento del curso, lecturas, casos escritos o guiones.

## Paquete según el NIVEL (si no se pidió, no se hace)
| Componente | Profesional | Experto |
|---|---|---|
| `presentacion.pptx` + `presentacion.json` | 12–18 diapositivas por hora, contenido real y notas de 80–200 palabras | 16–22 por hora, más comparaciones, lecturas comentadas y anexos |
| `investigacion.md` | Marcos, hallazgos, 3–5 casos reales, cifras, bibliografía APA (8–15 fuentes) | 6–10 casos, cifras trianguladas, debate académico, plan de actualización (20–35 fuentes) |
| `taller.md` (si se pidió) | Objetivo, instrucciones paso a paso, materiales o plantillas, tiempos, entregable, rúbrica | Igual, con caso real documentado, versión corta y larga, guía de facilitación |
| `quiz.md` (si se pidió) | 10 preguntas con retroalimentación por opción | 15–20 por dificultad, mapeadas a objetivos |
| `documento_curso.md/.docx` (si se pidió) | Contenido completo en prosa, por bloque | Más lecturas comentadas y glosario |
| `fuentes.md` | Siempre | Siempre |

## Diseño de la sesión
1. **Resultado de aprendizaje** en una frase, con verbo observable (Aplicar, Analizar, Diseñar).
   Es el que dijo la persona; si no lo dijo, Dumbledore lo preguntó.
2. **Bloques con tiempos** que suman la duración real. Por cada bloque: qué aprende, qué
   diapositivas lo cubren, qué interacción tiene (pregunta, ejercicio, caso) y cuánto dura.
3. **Secuencia (Gagné):** gancho con dato o pregunta → qué vamos a lograr → conceptos con
   ejemplos reales → caso → práctica guiada → síntesis → aplicación en el trabajo de cada uno →
   cierre.
4. **Una interacción cada 15–20 min**; en 2 horas, una pausa y al menos un ejercicio aplicado.
5. **Rigor según el público:** en posgrado, marcos con autor y año en la diapositiva, evidencia
   separada de opinión, bibliografía APA al final. En público empresarial, menos cita y más caso.

## Reglas de contenido
- **Cada diapositiva enseña algo por sí sola** (skill `presentacion-profesional`). Si al leer
  solo la diapositiva no se entiende la idea, está incompleta.
- **Casos reales con fuente,** del sector y la región que pidió la persona. Un caso = empresa,
  contexto, qué hizo, qué pasó, fuente con fecha, lección. Nunca ficticios ni "ilustrativos".
- **Cifras con fuente y fecha** en la diapositiva (`fuente`).
- **Datos propios** (nombre del programa, universidad, fecha, docente, logo del cliente) como
  `[COMPLETAR: …]`.
- **Ejemplos del trabajo real del público:** un fundador de SaaS, un gerente de pyme, un
  estudiante de maestría que trabaja; nada de ejemplos genéricos traducidos.
- **Lo que cambia rápido** (herramientas, precios, funciones de IA) se verifica el mismo día y
  se fecha.
- **Ética y seguridad** integradas cuando el tema lo toca (datos, Ley 1581, sesgos, alucinaciones).

## Entrega
- Todo lo final en `salidas/<tema>/` con los nombres de la tabla. `presentacion.json` va también,
  para poder editar y regenerar.
- `indice.md` corto: qué es cada archivo y en qué orden se usa para dictar.
