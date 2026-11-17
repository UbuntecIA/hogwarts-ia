# Listas de chequeo de calidad

> Las usa cada agente antes de entregar y McGonagall en la revisión final. El orden importa: lo
> primero es el cumplimiento del pedido; de nada sirve una pieza impecable que no es lo que se
> pidió. Un punto que no se cumple se corrige o se declara en el RESUMEN.

## 1. Cumplimiento del pedido (lo primero, siempre)
- [ ] Es **exactamente** el entregable principal de `ORDEN.md`: el tipo de pieza, para el
  público que dijo la persona (sin reinterpretarlo), con la extensión y el contenido acordados.
- [ ] Cumple cada punto de la **definición de terminado** de la ORDEN (cuéntalos uno por uno).
- [ ] **No hay nada de más:** ninguna pieza, sección o archivo que no se haya pedido o marcado.
- [ ] Lo opcional que la persona marcó está; lo que no marcó, no está.
- [ ] Sirve para el uso que dijo la persona (dictar, presentar a un cliente, publicar) sin
  rehacerlo: se puede abrir, leer de corrido y usar.

## 2. Verdad y fuentes
- [ ] **Nada inventado:** ni casos, ni empresas, ni cifras, ni citas, ni testimonios, ni
  "ejemplos ilustrativos". Cada caso tiene empresa real, fecha y fuente que se abrió.
- [ ] Toda cifra tiene fuente y fecha, en el texto y en `fuentes.md`. McGonagall abre al menos
  3 fuentes al azar y comprueba que digan lo que se les atribuye.
- [ ] Las fuentes son del tipo y la cantidad que exige el nivel (`conocimiento/niveles.md`).
- [ ] Los datos propios de ITERHUB o del cliente están como `[COMPLETAR: …]`, no supuestos.
- [ ] Lo que no se encontró está como `[DATO NO ENCONTRADO: …]`. No hay `SUPUESTO`, `BORRADOR`,
  `VERIFICAR` ni notas internas en las salidas.
- [ ] Lo que cambia rápido (herramientas de IA, precios, funciones de plataformas) se verificó
  con fecha.

## 3. Profundidad y oficio
- [ ] Cumple la profundidad del nivel para este tipo de pedido (`niveles.md`): cantidad de
  diapositivas o secciones, casos, variantes y anexos.
- [ ] Un profesional senior del área lo leería y no encontraría errores de fondo, vacíos ni
  generalidades. Nada que suene a plantilla.
- [ ] Aterrizado en el público real y, cuando aplica, en Colombia o Latinoamérica.
- [ ] Coherente de principio a fin: mismo público, misma promesa, mismas cifras y nombres.

## 4. Forma y marca
- [ ] Ortografía y gramática (tildes, ¿¡, concordancia). Tuteo. Claro y sin promesas exageradas.
- [ ] Marca ITERHUB (`configuracion/marca.md`): colores, tipografías, logos reales. El amarillo
  nunca es texto sobre blanco. Si es para un cliente, su marca va como `[COMPLETAR: logo y
  colores del cliente]` salvo que la persona los haya dado.
- [ ] Nombres de archivo claros y en `salidas/<tema>/`.

## 5. Cursos y talleres
- [ ] La PPT tiene las diapositivas que exige el nivel para la duración, y **cada una trae
  contenido real** (definición, pasos, dato, caso, pregunta o ejercicio), no viñetas sueltas.
- [ ] Cada diapositiva tiene notas del docente en prosa (80 a 200 palabras) que permiten
  dictarla.
- [ ] Hay una interacción cada 15 a 20 minutos y un cierre con aplicación.
- [ ] Los casos son reales, con fuente, y del sector o región que pidió la persona.
- [ ] En posgrado: marcos con autor y año; bibliografía APA al final.
- [ ] Taller y quiz solo si se pidieron, y completos (instrucciones, tiempos, entregable,
  rúbrica; retroalimentación por opción).
- [ ] `presentacion.json` y `presentacion.pptx` tienen el mismo número de diapositivas y el
  mismo contenido (nadie recortó al producir).

## 6. Estrategias, campañas y piezas
- [ ] Documento con la estructura de agencia (`marketing.md`): diagnóstico con datos reales,
  público, objetivos medibles, posicionamiento y mensajes, plan por canal, calendario,
  presupuesto, KPI, riesgos.
- [ ] Competencia con nombres reales y evidencia pública; nada de "competidores genéricos".
- [ ] Un objetivo y un llamado a la acción por pieza; gancho en la primera línea; límites
  reales del canal; variantes que cambian una sola cosa.
- [ ] Piezas listas para publicar **solo si se pidieron**.
- [ ] Datos personales, promociones y publicidad: Ley 1581 y Ley 1480 cuando aplique.

## 7. PPT, Word, HTML, JSON y prompts
- [ ] El `.pptx` abre; el número de diapositivas coincide con el JSON; sin texto desbordado
  (si no cabe, se divide la diapositiva).
- [ ] **Diseño:** al menos una de cada tres diapositivas es visual (diagrama, gráfico, iconos,
  línea de tiempo, imagen, cifras o caso); ninguna sección larga es solo texto; las gráficas
  tienen fuente; la portada tiene imagen o motivo de marca.
- [ ] Si hay diapositivas con imagen, existe `prompts_imagenes.md` con el nombre de archivo de
  cada una y la instrucción para regenerar la PPT.
- [ ] El `.docx` abre, tiene portada, títulos jerarquizados y tablas legibles.
- [ ] HTML se ve bien en celular y no depende de archivos inexistentes.
- [ ] El JSON carga con `json.load` y trae `instrucciones_para_la_ia`.
- [ ] Prompts de imagen adaptados a la IA que dijo la persona, con proporción, estilo y colores
  de marca; sin marcas ajenas ni personas reales.
