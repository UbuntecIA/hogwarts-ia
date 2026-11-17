# Hogwarts IA · la oficina de agentes de ITERHUB

Un castillo 3D de cinco pisos donde 24 personajes de Harry Potter son agentes de Claude Code.
Tú solo hablas con **Dumbledore**: él te hace las preguntas que cambian el resultado, te propone
un solo entregable, arma el equipo mínimo, **se aparece junto a cada agente para darle su misión**
(y le manda una lechuza con la carta), revisa todo y te entrega el resultado integrado.

## Los pisos
| Piso | Salas | Quién trabaja ahí |
|---|---|---|
| 4 · Torres altas | Despacho del Director, despacho de McGonagall, Lechucería, Torre de Astronomía | Dumbledore, McGonagall, Luna |
| 3 · Torre de Arte | Estudio de arte y cámaras, Sala de los Menesteres (reuniones por tarea) | Tonks, Dean, Colin |
| 2 · Aulas y salas comunes | Sala común de Gryffindor, Defensa, Encantamientos, Invernadero | Harry, Ron, Fred, George, Ginny, Lupin, Flitwick, Sprout |
| 1 · Planta baja | Gran Comedor (velas flotantes y techo encantado), Biblioteca, Vestíbulo | Hermione, Cho, Hagrid |
| 0 · Mazmorras | Aula de Pociones = Laboratorio de Código, Cocinas, Cámara de los Secretos | Snape, Draco, Bill, Neville, Arthur, Dobby, Voldemort |

Los pisos están en terrazas sobre el acantilado y se unen por la Gran Escalera. Con los botones
de abajo a la izquierda (o las teclas **0 a 4**) vuelas a cada piso; **C** muestra el castillo
completo. Toca a un personaje para ver su **mini bio, qué hace, cómo lo hace y su magia**, o toca
el suelo de una sala para ver qué se hace ahí.

## Qué le puedes pedir
- **Programar:** `/programa una landing con formulario para el webinar` (Snape, Draco, Bill, Arthur, Neville)
- **Videos:** `/video reel de 30 s sobre agentes de IA` (Colin) · `/videos-cortos …` (Ginny y Colin)
- **Contenido:** `/contenido artículo de blog sobre IA en ventas` (George) · `/pieza …` (Fred)
- **Presentaciones:** `/presentacion …` (Harry o Lupin escriben, Tonks dirige el arte, Dean o Sprout producen)
- **Investigar:** `/pedido investigación sobre …` (Hermione o Luna)
- **Cursos y talleres:** `/curso …`, `/taller …` · **Marketing:** `/campana …`, `/estrategia …`, `/lanzamiento …`
- **Reuniones:** botón **🕯 Convocar reunión**: eliges un equipo por tarea (programación,
  marketing, academia, video…) y caminan a la Sala de los Menesteres o al Gran Comedor. Puedes solo
  reunirlos (no gasta magia) o hacer una lluvia de ideas con acta (Voldemort ataca cada idea).

Cuando nadie trabaja, los agentes **pasean por todo Hogwarts**: cenan en el Gran Comedor, leen en
la biblioteca, se calientan en la chimenea, miran las estrellas o el lago. Cuando reciben una
misión vuelven a su puesto con **polvos flu** y lanzan hechizos (chispas) mientras trabajan.

## Puntos de magia (tokens)
Cada agente tiene una reserva diaria de **puntos de magia (PM)** que se recarga a medianoche.
**1 PM ≈ 1.000 tokens** ponderados por su costo real: entrada ×1, caché escrita ×1,25, caché
leída ×0,1 y salida ×5. La barrita bajo cada nombre muestra lo que le queda; al gastar sale un
"−3 ✨" sobre su cabeza. **✨ Magia hoy** abre el detalle por agente (hoy, histórico, misiones y
tokens). Se guarda en `oficina3d/magia.json`. Cuenta los pedidos hechos desde el castillo y
también los de `claude` en la terminal dentro de esta carpeta, siempre que el castillo esté
encendido. La reserva es un indicador: si se agota, el agente sigue trabajando y su barra se pone roja.

## Encenderlo
Necesitas Claude Code, Python 3 y **tu propia credencial de Claude** (sesión iniciada con `claude`,
o un token/clave en `.env`). La instalación paso a paso está en [README.md](README.md).
```
python3 oficina3d/servidor.py --abrir
```
Abre **http://localhost:8777** (o el puerto de `HOGWARTS_PUERTO` en `.env`). La primera vez ejecuta
`claude` dentro de esta carpeta y acepta confiar en ella; sin eso, Claude Code no avisa al castillo.
Para crear el ícono: `python3 oficina3d/crear_app.py`. **Ver demo** simula un pedido de
programación completo sin gastar magia de verdad.

## Reglas que no cambian
- Nada se inventa: casos, cifras y citas con fuente; lo que falte, `[DATO NO ENCONTRADO: …]`.
- Los datos de ITERHUB o del cliente quedan como `[COMPLETAR: …]`.
- Nada se publica, envía, pauta, despliega ni se conecta a cuentas reales.
- El personaje es solo el tono: los entregables van con la marca ITERHUB y **sin referencias a
  Harry Potter**, porque son para clientes reales. Los nombres y personajes son marcas de Warner
  Bros.; úsalos solo en esta oficina interna, no en material público de ITERHUB.

## Dónde está cada cosa
- `CLAUDE.md`: las instrucciones de Dumbledore. `configuracion/claude/`: agentes, comandos y skills
  (se copian a `.claude/` al encender el castillo). `conocimiento/`: lo que el equipo sabe.
- `oficina3d/equipo.js`: el elenco (bios, puestos, apariencia, reserva de magia).
- `pedidos/`: el trabajo de cada pedido. `salidas/<tema>/`: solo lo final.
