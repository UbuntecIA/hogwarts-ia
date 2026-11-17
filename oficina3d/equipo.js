// Hogwarts IA · el elenco de agentes (24). Fuente única para el castillo 3D y el servidor.
// slug = subagent_type de Claude Code (archivo .claude/agents/<slug>.md). "coordinador" es la sesión principal (Dumbledore).
// piso: 0 Mazmorras · 1 Planta baja · 2 Aulas y salas comunes · 3 Torre de arte y Sala de los Menesteres · 4 Torres altas
// reserva: puntos de magia (PM) por día. 1 PM ≈ 1.000 tokens ponderados por costo (salida ×5, caché leída ×0,1).
window.EQUIPO = [
 {
  "slug": "coordinador", "nombre": "Dumbledore", "nombreCompleto": "Albus Dumbledore",
  "cargo": "Director de Hogwarts IA · coordinador general", "area": "direccion", "num": "00",
  "piso": 4, "sala": "despacho", "reserva": 4000,
  "bio": "El único con quien hablas. Escucha con calma, pregunta lo justo y reparte cada misión a quien mejor la hará. Cuando delega, se aparece junto a cada agente para darle su tarea en persona y le envía una lechuza con la carta de la misión.",
  "hace": ["Te hace primero las preguntas que cambian el resultado.", "Propone un solo entregable principal, lo que incluye y lo que no.", "Arma el equipo mínimo y reparte misiones por oleadas.", "Integra, revisa la coherencia y te entrega todo junto."],
  "como": "Lee el pedido, consulta los libros de conocimiento, escribe la ORDEN con el plan por oleadas y visita a cada agente para entregarle su misión. Al final lo integra todo y te deja el resumen.",
  "entrega": "RESUMEN.md y la entrega integrada",
  "apariencia": {"piel": "F1C9A5", "pelo": "E8E8EC", "peinado": "largo", "barba": "larga", "sombrero": "puntiagudo", "sombreroColor": "4B2A7B", "gafas": "medialuna", "tunica": "5B2C8F", "forro": "C9A227", "escala": 1.08}
 },
 {
  "slug": "revision-editorial", "nombre": "McGonagall", "nombreCompleto": "Minerva McGonagall",
  "cargo": "Subdirectora · control de calidad", "area": "direccion", "num": "99",
  "piso": 4, "sala": "mcgonagall", "reserva": 2000,
  "bio": "Exigente y justa. Nada sale de Hogwarts IA sin pasar por su escritorio. Su primera pregunta siempre es la misma: ¿esto es exactamente lo que se pidió?",
  "hace": ["Revisa la definición de terminado punto por punto.", "Abre fuentes al azar y comprueba que digan lo que se cita.", "Bloquea cualquier caso, cifra o testimonio inventado.", "Devuelve cambios precisos a cada autor o aprueba."],
  "como": "Trabaja con la ORDEN al lado y una lista de chequeo. Califica como en un examen: APROBADO o CAMBIOS, con el motivo exacto.",
  "entrega": "revision.md (APROBADO o CAMBIOS)",
  "apariencia": {"piel": "EFCFB4", "pelo": "3A3A3A", "peinado": "mono", "sombrero": "puntiagudo", "sombreroColor": "1F5B3A", "gafas": "cuadradas", "tunica": "1F5B3A", "forro": "0F2E1D", "escala": 1.02}
 },
 {
  "slug": "abogado-diablo", "nombre": "Voldemort", "nombreCompleto": "Lord Voldemort",
  "cargo": "Abogado del diablo · pruebas de estrés", "area": "direccion", "num": "98",
  "piso": 0, "sala": "camara", "reserva": 1500,
  "bio": "Vive en la Cámara de los Secretos y no tiene piedad con las ideas débiles. Ataca cada plan como lo haría el peor cliente, el competidor más duro o el estudiante más escéptico, para que llegue blindado.",
  "hace": ["Busca los puntos débiles de estrategias, cursos y código.", "Simula objeciones del cliente, la competencia y el público.", "Señala riesgos legales, de reputación y de datos.", "Propone cómo blindar cada punto, no solo critica."],
  "como": "Lee el entregable como enemigo, escribe las diez peores preguntas que alguien podría hacer y para cada una propone la defensa. Asiste a toda reunión de ideas.",
  "entrega": "ataque.md (objeciones, riesgos y defensas)",
  "apariencia": {"piel": "DCE3E3", "pelo": null, "peinado": "calvo", "sinNariz": true, "ojosRojos": true, "tunica": "121214", "forro": "1E3B2A", "escala": 1.1}
 },
 {
  "slug": "guardabosques", "nombre": "Hagrid", "nombreCompleto": "Rubeus Hagrid",
  "cargo": "Guardián de llaves · entregas y archivo", "area": "direccion", "num": "97",
  "piso": 1, "sala": "vestibulo", "reserva": 800,
  "bio": "El guardián de las llaves y los terrenos. Al final de cada pedido empaca la entrega: ordena salidas/, escribe el paquete para otros agentes y verifica que no falte ningún archivo.",
  "hace": ["Verifica que existan todos los archivos de la entrega.", "Escribe PARA_OTROS_AGENTES.md con rutas completas.", "Ordena salidas/<tema>/ y quita borradores.", "Lleva el inventario de lo entregado."],
  "como": "Recorre la carpeta de salidas con la lista de la ORDEN en la mano y no la cierra hasta que todo esté en su sitio.",
  "entrega": "PARA_OTROS_AGENTES.md y salidas ordenadas",
  "apariencia": {"piel": "E7BE9A", "pelo": "2A1B12", "peinado": "melena", "barba": "tupida", "tunica": "4A3524", "forro": "2E2014", "escala": 1.5}
 },
 {
  "slug": "estratega-marca", "nombre": "Harry", "nombreCompleto": "Harry Potter",
  "cargo": "Estratega de marketing · capitán de Marketing", "area": "marketing", "num": "01",
  "piso": 2, "sala": "gryffindor", "reserva": 2500, "coordina": "marketing",
  "bio": "Capitán del equipo de Marketing. Ve la jugada completa como un buscador ve la snitch: el objetivo de negocio. Es el dueño de toda estrategia y documento de campaña.",
  "hace": ["Diagnóstico con datos reales y competencia con nombres.", "Posicionamiento, mensajes y plan por canal.", "Calendario, presupuesto por escenarios y KPI.", "Escribe el guion de la PPT para presentar la estrategia."],
  "como": "Parte de la investigación de Luna, define una sola apuesta, la convierte en plan de 90 días y coordina a Ron, Fred, George y Ginny.",
  "entrega": "estrategia.md o campana.md (y presentacion.json)",
  "apariencia": {"piel": "F0C8A8", "pelo": "17110D", "peinado": "despeinado", "gafas": "redondas", "cicatriz": true, "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["7F0909", "D3A625"], "escala": 0.96}
 },
 {
  "slug": "investigacion-audiencias", "nombre": "Luna", "nombreCompleto": "Luna Lovegood",
  "cargo": "Investigadora de mercado y audiencias", "area": "marketing", "num": "02",
  "piso": 4, "sala": "astronomia", "reserva": 2000,
  "bio": "Ve lo que nadie más ve en una audiencia, pero solo cree en lo que puede comprobar. Desde la Torre de Astronomía rastrea mercados, competidores y tendencias con fuentes reales.",
  "hace": ["Busca en fuentes oficiales, informes, prensa y bibliotecas de anuncios.", "Abre y verifica cada fuente antes de citarla.", "Arma perfiles de audiencia con evidencia, no con intuición.", "Registra todo en fuentes.md."],
  "como": "Hace preguntas raras que nadie hizo, las busca en la web, anota cada hallazgo con su fuente y fecha, y separa lo comprobado de lo que no encontró.",
  "entrega": "investigacion_mercado.md y fuentes.md",
  "apariencia": {"piel": "F6DCC7", "pelo": "EAD9A0", "peinado": "largoSuelto", "tunica": "1B1B22", "forro": "0E1A40", "bufanda": ["0E1A40", "946B2D"], "escala": 0.94}
 },
 {
  "slug": "copywriter", "nombre": "Fred", "nombreCompleto": "Fred Weasley",
  "cargo": "Redactor creativo · copys y ganchos", "area": "marketing", "num": "03",
  "piso": 2, "sala": "gryffindor", "reserva": 1500,
  "bio": "Una mitad de los gemelos más ingeniosos de Hogwarts. Convierte cualquier estrategia en frases que la gente quiere leer: ganchos, copys por canal y variantes para probar.",
  "hace": ["Mensajes clave a partir de la estrategia de Harry.", "Copys por canal con límites reales y un solo llamado a la acción.", "Variantes que cambian una sola cosa para probar.", "Nada inventado: ofertas y precios como [COMPLETAR]."],
  "como": "Escribe diez ganchos, se queda con tres, los afina por canal y los prueba en voz alta con George.",
  "entrega": "copys.md",
  "apariencia": {"piel": "F3CDB0", "pelo": "C2491D", "peinado": "corto", "pecas": true, "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["7F0909", "D3A625"], "escala": 1.04}
 },
 {
  "slug": "contenido-web", "nombre": "George", "nombreCompleto": "George Weasley",
  "cargo": "Creador de contenido largo · blogs, newsletters y SEO", "area": "marketing", "num": "08",
  "piso": 2, "sala": "gryffindor", "reserva": 1500,
  "bio": "La otra mitad de los gemelos. Donde Fred escribe frases, George escribe artículos, newsletters, guías y ebooks que posicionan en buscadores y se leen hasta el final.",
  "hace": ["Artículos de blog y guías con SEO real (intención de búsqueda).", "Newsletters y secuencias de correo.", "Ebooks, lead magnets y textos de landing page.", "Todo con fuentes y datos verificados."],
  "como": "Investiga qué busca la gente, arma la estructura con títulos claros, escribe con ejemplos reales y deja meta título, descripción y enlaces sugeridos.",
  "entrega": "articulos/ y contenido.md",
  "apariencia": {"piel": "F3CDB0", "pelo": "C2491D", "peinado": "corto", "pecas": true, "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["D3A625", "7F0909"], "escala": 1.04}
 },
 {
  "slug": "redes-sociales", "nombre": "Ginny", "nombreCompleto": "Ginny Weasley",
  "cargo": "Redes sociales y WhatsApp", "area": "marketing", "num": "04",
  "piso": 2, "sala": "gryffindor", "reserva": 1500,
  "bio": "Capitana en la cancha y en las redes. Sabe qué formato está funcionando hoy en LinkedIn, Instagram, TikTok y WhatsApp, y arma calendarios que se pueden publicar.",
  "hace": ["Investiga tendencias y referentes reales de cada canal.", "Arma calendarios de contenido con gancho, pieza y KPI.", "Escribe guiones de video corto para redes.", "Diseña listas y plantillas de WhatsApp con consentimiento."],
  "como": "Revisa qué publican hoy los referentes del sector, elige formatos y escribe cada pieza con su gancho de 2 segundos y su métrica.",
  "entrega": "calendario_redes.md y guiones",
  "apariencia": {"piel": "F3CDB0", "pelo": "B5361A", "peinado": "largoSuelto", "pecas": true, "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["7F0909", "D3A625"], "escala": 0.93}
 },
 {
  "slug": "pauta-digital", "nombre": "Ron", "nombreCompleto": "Ron Weasley",
  "cargo": "Pauta digital en Meta · estrategia de medios", "area": "marketing", "num": "05",
  "piso": 2, "sala": "gryffindor", "reserva": 1500,
  "bio": "El mejor jugador de ajedrez de Hogwarts. Planea la pauta como una partida: qué pieza mover, cuánto sacrificar y cuándo atacar. Nunca lanza ni gasta: deja el plan listo.",
  "hace": ["Define objetivo y estructura de campaña en Meta.", "Segmentación justificada y formatos por ubicación.", "Presupuesto con CPM, CPC y CPL de referencia con fuente.", "Pruebas A/B, píxel, eventos y UTM."],
  "como": "Arma tres escenarios de presupuesto (prudente, base y agresivo), calcula cuántos resultados compra cada uno y deja claro qué medir cada semana.",
  "entrega": "plan_pauta.md",
  "apariencia": {"piel": "F3CDB0", "pelo": "D4561E", "peinado": "corto", "pecas": true, "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["7F0909", "D3A625"], "escala": 1.08}
 },
 {
  "slug": "diseno-instruccional", "nombre": "Lupin", "nombreCompleto": "Remus Lupin",
  "cargo": "Diseñador de cursos · coordina Academia", "area": "academia", "num": "11",
  "piso": 2, "sala": "defensa", "reserva": 2500, "coordina": "academia",
  "bio": "El profesor que todos recuerdan. Diseña cada curso, clase o taller para que se entienda a la primera y escribe el contenido real de cada diapositiva con las notas del docente.",
  "hace": ["Resultado de aprendizaje y bloques con tiempos.", "Escribe cada diapositiva con contenido real y notas de 80 a 200 palabras.", "Usa solo casos reales del dossier de Hermione.", "Deja el momento exacto del taller o el quiz si se pidieron."],
  "como": "Empieza por lo que el estudiante debe poder hacer al salir, ordena los bloques en esa dirección y mete una interacción cada 15 a 20 minutos.",
  "entrega": "estructura.md y presentacion.json",
  "apariencia": {"piel": "E9C9AE", "pelo": "8A7356", "peinado": "corto", "barba": "sombra", "tunica": "5E5546", "forro": "3E382D", "escala": 1.03}
 },
 {
  "slug": "investigacion-tematica", "nombre": "Hermione", "nombreCompleto": "Hermione Granger",
  "cargo": "Investigadora académica", "area": "academia", "num": "12",
  "piso": 1, "sala": "biblioteca", "reserva": 2500,
  "bio": "Ha leído todos los libros de la biblioteca y sabe exactamente dónde está cada dato. Construye el dossier sobre el que se enseña: marcos con autor y año, casos reales y bibliografía APA.",
  "hace": ["Fuentes oficiales, académicas, informes, artículos y revistas.", "Abre y lee cada fuente antes de citarla.", "Casos reales: empresa, qué hizo, qué pasó, fuente y lección.", "Marca lo que no encontró; nunca inventa."],
  "como": "Planea las preguntas, busca en varias fuentes, triangula cada cifra, la anota con fecha y deja la bibliografía impecable.",
  "entrega": "investigacion.md y fuentes.md",
  "apariencia": {"piel": "F2CBAA", "pelo": "6B3E1E", "peinado": "rizado", "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["7F0909", "D3A625"], "escala": 0.95}
 },
 {
  "slug": "lecciones-guiones", "nombre": "Cho", "nombreCompleto": "Cho Chang",
  "cargo": "Redactora académica · documentos y lecturas", "area": "academia", "num": "15",
  "piso": 1, "sala": "biblioteca", "reserva": 1500,
  "bio": "Ravenclaw de pluma clara. Cuando se pide material escrito, convierte el curso en documentos que se leen fácil: prosa completa, lecturas, casos escritos y guías del docente.",
  "hace": ["Documento del curso completo por bloque, listo para Word.", "Lecturas y casos escritos para el estudiante.", "Guías extendidas del docente.", "Mismas fuentes y citas que la PPT."],
  "como": "Toma la estructura de Lupin y el dossier de Hermione, y escribe bloque por bloque con ejemplos y preguntas de reflexión.",
  "entrega": "documento_curso.md y lecturas",
  "apariencia": {"piel": "EED2B0", "pelo": "121212", "peinado": "largoSuelto", "tunica": "1B1B22", "forro": "0E1A40", "bufanda": ["0E1A40", "946B2D"], "escala": 0.94}
 },
 {
  "slug": "laboratorios-ia", "nombre": "Flitwick", "nombreCompleto": "Filius Flitwick",
  "cargo": "Diseñador de talleres, ejercicios y quiz", "area": "academia", "num": "13",
  "piso": 2, "sala": "encantamientos", "reserva": 1500,
  "bio": "Pequeño de estatura y enorme en la práctica. Cuando se pide un taller o un quiz, lo diseña completo: caso real, instrucciones, plantillas, tiempos y rúbrica.",
  "hace": ["Taller alineado con los bloques de Lupin.", "Plantillas y lienzos en Markdown y Word.", "Rúbricas con criterios observables.", "Quiz de aplicación con retroalimentación por opción."],
  "como": "Prueba cada ejercicio como si fuera el estudiante: si no se puede hacer en el tiempo dado, lo ajusta.",
  "entrega": "taller.md, plantillas y quiz.md",
  "apariencia": {"piel": "F0CBA9", "pelo": "D9D9D9", "peinado": "corto", "barba": "bigote", "tunica": "2B3A67", "forro": "946B2D", "escala": 0.62}
 },
 {
  "slug": "material-clase", "nombre": "Sprout", "nombreCompleto": "Pomona Sprout",
  "cargo": "Productora de material de clase · PPT y Word", "area": "academia", "num": "14",
  "piso": 2, "sala": "invernadero", "reserva": 1500,
  "bio": "Cultiva el material con paciencia de jardinera: convierte el guion de Lupin en la PPT final y el Word sin cortar una sola hoja. Si algo no cabe, divide la diapositiva.",
  "hace": ["Genera la PPT y comprueba que abra y coincida con el guion.", "Mejora el tipo de diapositiva sin cambiar el texto.", "Produce el Word del curso o del taller.", "Plantillas del taller listas para imprimir."],
  "como": "Ejecuta las herramientas de PPT y Word, abre el resultado, cuenta las diapositivas y lo compara con el guion antes de entregarlo.",
  "entrega": "presentacion.pptx, .docx y plantillas",
  "apariencia": {"piel": "EFC6A2", "pelo": "8E8B7E", "peinado": "rizadoCorto", "sombrero": "parchado", "sombreroColor": "6B5B2E", "tunica": "6B5B2E", "forro": "ECB939", "escala": 0.9}
 },
 {
  "slug": "direccion-arte", "nombre": "Tonks", "nombreCompleto": "Nymphadora Tonks",
  "cargo": "Directora de arte · imágenes y estilo visual", "area": "produccion", "num": "07",
  "piso": 3, "sala": "arte", "reserva": 1500,
  "bio": "Cambia de apariencia a voluntad, y lo mismo hace con cada presentación. Decide qué diapositivas llevan imagen y escribe los prompts completos para que la IA de imágenes las genere.",
  "hace": ["Plan visual de cada PPT: imagen, diagrama, gráfica o línea de tiempo.", "Mínimo una imagen de cada tres diapositivas.", "Prompts completos con escena, encuadre, fondo y paleta.", "Deja prompts_imagenes.md y .json listos."],
  "como": "Lee el guion sin cambiar una palabra, alterna imágenes con diagramas para que no se repita y escribe cada prompt como una orden de rodaje.",
  "entrega": "prompts_imagenes.md y .json",
  "apariencia": {"piel": "F3D2B8", "pelo": "E0479E", "peinado": "puntas", "tunica": "2A2A2E", "forro": "ECB939", "escala": 0.96}
 },
 {
  "slug": "diseno-grafico", "nombre": "Dean", "nombreCompleto": "Dean Thomas",
  "cargo": "Productor de presentaciones y piezas gráficas", "area": "produccion", "num": "06",
  "piso": 3, "sala": "arte", "reserva": 1500,
  "bio": "El artista de Gryffindor. Produce la PPT, el Word y las piezas visuales de Marketing (carruseles, banners, historias) con la marca real, sin recortar el contenido de quien lo escribió.",
  "hace": ["Genera y verifica la PPT desde el guion de Harry.", "Produce el Word desde el documento final.", "Piezas HTML de redes (carrusel, banner, historia) si se pidieron.", "JSON para otra IA si se pidió."],
  "como": "Arma la pieza, la abre, revisa cada diapositiva o lámina contra el guion y la marca, y solo entonces la entrega.",
  "entrega": "presentacion.pptx, .docx y piezas",
  "apariencia": {"piel": "6B4228", "pelo": "1A120C", "peinado": "rapado", "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["7F0909", "D3A625"], "escala": 1.05}
 },
 {
  "slug": "produccion-video", "nombre": "Colin", "nombreCompleto": "Colin Creevey",
  "cargo": "Productor de video", "area": "produccion", "num": "31",
  "piso": 3, "sala": "arte", "reserva": 2000,
  "bio": "Nunca suelta la cámara. Convierte una idea en video: guion, guion gráfico, lista de planos, prompts para IAs de video, y si le pasas tus grabaciones, las edita con subtítulos y formato vertical.",
  "hace": ["Guion técnico y guion gráfico plano por plano.", "Prompts para IAs de video (Sora, Veo, Runway, Kling).", "Edición con ffmpeg: cortes, subtítulos, vertical, música y logo.", "Subtítulos .srt y textos para publicar."],
  "como": "Escribe el video segundo a segundo, decide qué se graba y qué genera la IA, y si hay material propio lo monta con ffmpeg y revisa el resultado.",
  "entrega": "guion_video.md, prompts_video.json y videos editados",
  "apariencia": {"piel": "F3D3BA", "pelo": "B88A4A", "peinado": "corto", "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["7F0909", "D3A625"], "camara": true, "escala": 0.82}
 },
 {
  "slug": "tareas-rapidas", "nombre": "Dobby", "nombreCompleto": "Dobby",
  "cargo": "Elfo de tareas rápidas · ajustes y formatos", "area": "produccion", "num": "90",
  "piso": 0, "sala": "cocinas", "reserva": 800,
  "bio": "Elfo libre y el más rápido de Hogwarts. Se encarga de lo pequeño que no puede esperar: convertir formatos, renombrar, ordenar carpetas, corregir un dato o regenerar una PPT.",
  "hace": ["Ajustes pequeños sobre entregas ya hechas.", "Conversión de formatos (Markdown, Word, PPT, JSON).", "Ordenar y renombrar archivos en salidas/.", "Regenerar la PPT cuando llegan las imágenes."],
  "como": "Hace exactamente lo que se le pidió, sin agregar nada, y avisa qué cambió.",
  "entrega": "el ajuste pedido",
  "apariencia": {"piel": "C9C1A6", "pelo": null, "peinado": "calvo", "orejas": true, "ojosGrandes": true, "tunica": "D9D2BC", "forro": "8E865F", "escala": 0.55}
 },
 {
  "slug": "arquitectura-software", "nombre": "Snape", "nombreCompleto": "Severus Snape",
  "cargo": "Arquitecto de software · jefe del Laboratorio de Código", "area": "tecnologia", "num": "21",
  "piso": 0, "sala": "pociones", "reserva": 3000, "coordina": "tecnologia",
  "bio": "La programación es como las pociones: una medida de más y todo explota. Diseña la arquitectura, divide el trabajo entre su equipo y revisa cada línea de código antes de que salga de las mazmorras.",
  "hace": ["Arquitectura, stack y estructura de carpetas.", "Plan de tareas para frontend, backend, automatización y pruebas.", "Revisión de código: errores, seguridad y simplicidad.", "Decide cuándo el código está listo."],
  "como": "Escribe ARQUITECTURA.md con decisiones justificadas y una lista de tareas verificables; al final lee todo el código y devuelve correcciones exactas.",
  "entrega": "ARQUITECTURA.md y revision_codigo.md",
  "apariencia": {"piel": "E8D6C2", "pelo": "0E0E10", "peinado": "cortina", "tunica": "0C0C0F", "forro": "1A472A", "escala": 1.06}
 },
 {
  "slug": "desarrollo-frontend", "nombre": "Draco", "nombreCompleto": "Draco Malfoy",
  "cargo": "Desarrollador frontend · interfaces", "area": "tecnologia", "num": "22",
  "piso": 0, "sala": "pociones", "reserva": 2000,
  "bio": "Exige que todo se vea impecable, y lo consigue. Construye las interfaces: páginas, apps y paneles rápidos, accesibles y que funcionan en el celular.",
  "hace": ["Interfaces en HTML, CSS, JavaScript, React o lo que pida la arquitectura.", "Diseño responsive y accesible.", "Conecta la interfaz con la API de Bill.", "Prueba cada pantalla en el navegador."],
  "como": "Sigue ARQUITECTURA.md al pie de la letra, construye componente por componente y no da nada por terminado sin abrirlo y probarlo.",
  "entrega": "código de la interfaz en salidas/<tema>/",
  "apariencia": {"piel": "F4DCC8", "pelo": "EDE3C5", "peinado": "peinadoAtras", "tunica": "1B1B22", "forro": "1A472A", "bufanda": ["1A472A", "AAAAAA"], "escala": 1.0}
 },
 {
  "slug": "desarrollo-backend", "nombre": "Bill", "nombreCompleto": "Bill Weasley",
  "cargo": "Desarrollador backend · datos y APIs", "area": "tecnologia", "num": "23",
  "piso": 0, "sala": "pociones", "reserva": 2000,
  "bio": "Rompedor de maldiciones en Gringotts: sabe proteger bóvedas. Construye servidores, APIs y bases de datos seguras, con datos que no se pierden.",
  "hace": ["APIs, servidores y lógica de negocio.", "Modelos de datos y bases de datos.", "Autenticación y manejo seguro de secretos.", "Scripts de datos en Python o Node."],
  "como": "Define primero los datos y los contratos de la API, luego implementa con pruebas pequeñas para cada función.",
  "entrega": "código del backend en salidas/<tema>/",
  "apariencia": {"piel": "F3CDB0", "pelo": "C2491D", "peinado": "coleta", "tunica": "3A2A20", "forro": "7F0909", "escala": 1.07}
 },
 {
  "slug": "pruebas-qa", "nombre": "Neville", "nombreCompleto": "Neville Longbottom",
  "cargo": "Pruebas y calidad del código", "area": "tecnologia", "num": "24",
  "piso": 0, "sala": "pociones", "reserva": 1500,
  "bio": "Paciente y valiente. Cultiva pruebas como plantas: escribe las pruebas, las ejecuta, encuentra lo que se rompe y no se rinde hasta que todo pasa.",
  "hace": ["Plan de pruebas a partir de lo que se pidió.", "Pruebas automáticas y manuales.", "Ejecuta todo y reporta errores con pasos para reproducirlos.", "Verifica que cada corrección de verdad funcione."],
  "como": "Para cada requisito escribe al menos una prueba, las corre de verdad y entrega un informe con lo que pasó y lo que falló.",
  "entrega": "pruebas/ e informe_pruebas.md",
  "apariencia": {"piel": "F2CEB0", "pelo": "5A3A22", "peinado": "corto", "tunica": "1B1B22", "forro": "7F0909", "bufanda": ["7F0909", "D3A625"], "escala": 1.0}
 },
 {
  "slug": "automatizaciones", "nombre": "Arthur", "nombreCompleto": "Arthur Weasley",
  "cargo": "Integraciones y automatizaciones", "area": "tecnologia", "num": "25",
  "piso": 0, "sala": "pociones", "reserva": 1500,
  "bio": "Le fascina cómo funcionan los aparatos muggles. Conecta herramientas entre sí: APIs, webhooks, hojas de cálculo, CRMs, n8n, Zapier o Make, y scripts que ahorran horas.",
  "hace": ["Flujos de automatización paso a paso (n8n, Make, Zapier).", "Integraciones con APIs y webhooks.", "Scripts para mover, limpiar y transformar datos.", "Manual de cómo conectarlo con las claves de la persona."],
  "como": "Dibuja el flujo de punta a punta, prueba cada paso con datos de ejemplo y deja los espacios de claves como [COMPLETAR].",
  "entrega": "flujos .json, scripts y AUTOMATIZACION.md",
  "apariencia": {"piel": "F3CDB0", "pelo": "C2491D", "peinado": "entradas", "gafas": "redondas", "tunica": "5A4632", "forro": "7F0909", "escala": 1.02}
 }
];
