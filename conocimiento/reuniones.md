# Reuniones de ideas (lluvia de ideas en la sala de juntas)

Cuando la persona trae un reto o una necesidad y quiere **ideas** (no una pieza terminada), el
equipo se reúne en la sala de juntas. Cada asistente opina **desde su especialidad**, y al final
sale un **acta** con las ideas priorizadas y los siguientes pasos.

## Asistentes
| Rol en la reunión | Quién | Qué aporta |
|---|---|---|
| **Moderador** | Dumbledore | Formula el reto, convoca, agrupa ideas, prioriza y escribe el acta |
| **Evaluadora** | McGonagall | Viabilidad, marca, calidad y confianza de cada idea (sombrero negro) |
| **Abogado del diablo** | Voldemort | Ataca cada idea como el peor cliente, la competencia o el público más escéptico (incluidos riesgos legales: Ley 1581, Ley 1480) y propone cómo blindarla |
| **Coordinador de Marketing** | Harry | Ideas propias y, en la segunda ronda, combina las ideas de Marketing |
| **Coordinador de Academia** | Lupin | Ideas propias y, en la segunda ronda, combina las ideas de Academia |
| **Coordinador de Tecnología** | Snape (solo si el tema es de tecnología) | Ideas propias y, en la segunda ronda, combina las ideas de tecnología |
| **Especialistas invitados** | 2 a 4 según el tema | Ideas desde su oficio |

**Cómo se eligen los asistentes:**
- Si el pedido trae una línea `Asistentes: …`, esos son los asistentes (más Dumbledore como
  moderador).
- Si no, asisten siempre Dumbledore, McGonagall, Voldemort, Harry y Lupin; Snape si el tema es
  de tecnología (software, automatización, datos, páginas o apps); y 2 a 4 especialistas que
  Dumbledore elige según el tema. Por ejemplo:
  - para conseguir inscritos o vender: Luna, Fred, Ginny y Ron;
  - para un curso o taller nuevo: Hermione, Flitwick y Cho;
  - para contenido y redes: Ginny, Fred, George y Colin;
  - para un cliente nuevo: Luna, Ron y Hermione;
  - para una herramienta, app o automatización: Draco, Bill, Arthur y Neville.
- Si la persona nombra especialistas, se invita a esos.
- Máximo 9 personas en la mesa.

## Técnicas (cada participante usa la que mejor le sirva)
- **"¿Cómo podríamos…?":** convierte el problema en una pregunta abierta. Ejemplo: "¿Cómo
  podríamos lograr que 200 dueños de pymes se inscriban al webinar sin pauta paga?".
- **SCAMPER** (para mejorar algo que ya existe):
  - **S**ustituir;
  - **C**ombinar;
  - **A**daptar;
  - **M**odificar o magnificar;
  - **P**oner en otro uso;
  - **E**liminar;
  - **R**eordenar o invertir.
- **Los 6 sombreros de De Bono:**
  - blanco: datos;
  - rojo: emoción;
  - negro: riesgos (es el de McGonagall y Voldemort);
  - amarillo: beneficios;
  - verde: creatividad;
  - azul: proceso (es el de Dumbledore).
- **Pensamiento inverso:** "¿Qué haríamos para que esto fracase seguro?" y luego se invierte
  cada respuesta.
- **Analogías:** "¿Cómo lo resolvería Duolingo, Netflix o una tienda de barrio?".
- **Restricción creativa:** "¿Y si tuviéramos 0 pesos?" o "¿Y si tuviéramos solo una semana?".

**Reglas de la primera ronda:**
- Cantidad antes que calidad.
- Nada se critica todavía.
- Cada idea debe ser concreta (qué, para quién y el primer paso).
- Al menos una idea "loca" por persona.

## Priorización
**Puntaje ICE** (de 1 a 10 en cada criterio):
- **I**mpacto: ¿cuánto mueve el objetivo?
- **C**onfianza: ¿qué tan seguros estamos de que funciona? Hay evidencia, casos o datos.
- **F**acilidad: ¿qué tan fácil y barato es hacerlo? 10 significa que se puede hacer esta semana
  con lo que hay.

El puntaje ICE es el promedio de los tres.

**Matriz impacto/esfuerzo:**
- Victorias rápidas: impacto alto, esfuerzo bajo.
- Apuestas grandes: impacto alto, esfuerzo alto.
- Rellenos: impacto bajo, esfuerzo bajo.
- Descartar: impacto bajo, esfuerzo alto.

McGonagall marca con ⚠ las ideas con riesgo legal, de marca o reputacional, y la confianza de esas
ideas baja. Voldemort agrega el ataque más duro a cada idea y cómo blindarla; una idea que no
resiste el ataque baja su confianza.

## El acta (`ACTA.md`, que también es el `RESUMEN.md` de la reunión)
```markdown
# Acta de reunión: <tema>
**Fecha:** · **Asistentes:** Dumbledore (moderador), McGonagall (evaluadora), Voldemort (abogado del diablo), Harry, Lupin, …
## El reto
<La necesidad tal como la planteó la persona + la pregunta "¿Cómo podríamos…?">
## Lo que propuso cada uno
### Harry (estrategia de marketing)
- Idea 1 …
…
## Ideas combinadas (segunda ronda)
## Evaluación de McGonagall
<riesgos ⚠ y condiciones>
## Ataque de Voldemort
<el ataque más duro a cada idea y cómo blindarla>
## Priorización
| # | Idea | Autor(es) | I | C | F | ICE | Cuadrante |
## Recomendación
<Top 3 ideas, por qué, y la victoria rápida para empezar esta semana>
## Siguientes pasos
| Acción | Responsable (agente o persona) | Pedido sugerido |
| Desarrollar idea 1 | Fred + Dean | `/campana …` |
## Preguntas abiertas para ti
```
