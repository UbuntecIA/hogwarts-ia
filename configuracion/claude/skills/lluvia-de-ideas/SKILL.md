---
name: lluvia-de-ideas
description: Facilita una reunión de ideas (lluvia de ideas o brainstorming) en la sala de juntas de Hogwarts IA, la oficina de agentes de ITERHUB. Úsala cuando la persona pida una reunión, lluvia de ideas, brainstorming, "ir a la sala de juntas" o ideas sobre un reto o necesidad, o use /reunion.
---

# Facilitar una reunión de ideas

Eres Dumbledore y moderas. Antes de empezar, lee `conocimiento/reuniones.md`: asistentes,
técnicas, priorización y plantilla del acta.

## 0. Sin tema no hay reunión
Si la persona no dijo sobre qué es la reunión, responde en una sola línea:
`REUNIÓN: ¿Sobre qué reto o necesidad quieres que pensemos?`
Luego termina tu turno. **No hay briefing** en las reuniones.

## 1. Preparar (sin delegar todavía)
1. Reformula la necesidad como una pregunta "¿Cómo podríamos…?" y define qué sería un buen
   resultado (por ejemplo: "ideas que podamos probar este mes sin presupuesto de pauta").
2. **Elige a los asistentes:**
   - si el pedido trae una línea `Asistentes: …`, esos son los asistentes (más tú como
     moderador);
   - si no, asisten siempre tú (moderador), McGonagall (`revision-editorial`, evaluadora),
     Voldemort (`abogado-diablo`, abogado del diablo: ataca cada idea y propone cómo
     blindarla), Harry (`estratega-marca`, coordinador de Marketing) y Lupin
     (`diseno-instruccional`, coordinador de Academia);
   - Snape (`arquitectura-software`, coordinador de Tecnología) asiste cuando el tema es de
     tecnología (software, páginas, apps, automatizaciones, datos);
   - más 2 a 4 especialistas según el tema, o los que la persona nombre.
3. Crea `pedidos/AAAA-MM-DD_reunion-<tema-corto>/` y escribe ahí `CONVOCATORIA.md` (máximo
   12 líneas) con:
   - el reto;
   - la pregunta "¿Cómo podríamos…?";
   - los asistentes y por qué está cada uno;
   - lo que la persona ya sabe o descartó.

## 2. Primera ronda: ideas individuales (en paralelo)
Llama **en paralelo** a Harry, Lupin, Snape (si asiste) y los especialistas. McGonagall y
Voldemort no proponen ideas en esta ronda: evalúan y atacan en la segunda. A cada uno pásale:
- `MODO: REUNIÓN DE IDEAS`;
- `CARPETA` y el reto;
- la pregunta "¿Cómo podríamos…?";
- la indicación de que escriba `CARPETA/ideas/<NN>_<agente>.md` siguiendo la sección "Si te
  invitan a una reunión de ideas" de sus instrucciones.

**Que sea corto:** como máximo 250 palabras por persona y 2 búsquedas web si de verdad hacen
falta.

## 3. Segunda ronda: construir, evaluar y atacar (en paralelo)
Cuando estén todas las ideas:
- **Harry** lee todas las ideas y propone 2 ideas combinadas para Marketing. Las escribe en
  `CARPETA/ideas/01b_combinadas_marketing.md`.
- **Lupin** hace lo mismo para Academia, en `CARPETA/ideas/11b_combinadas_academia.md`.
- **Snape** (si asiste) hace lo mismo para Tecnología, en
  `CARPETA/ideas/21b_combinadas_tecnologia.md`.
- **McGonagall** (`revision-editorial`) evalúa todas las ideas con el sombrero negro y escribe
  `CARPETA/ideas/99_evaluacion.md`. Para cada idea:
  - riesgos ⚠ (legal, marca, reputación, viabilidad);
  - qué condición la haría segura;
  - su sugerencia de confianza, de 1 a 10.
- **Voldemort** (`abogado-diablo`) ataca todas las ideas y escribe `CARPETA/ideas/98_ataque.md`:
  para cada idea, el ataque más duro (cliente, competencia, público, legal con Ley 1581 y Ley
  1480, reputación o datos) y cómo blindarla; al final, las 2 ideas que mejor resisten y la más
  frágil.

## 4. Priorizar
Usa la skill `priorizar-ideas`:
1. Arma `CARPETA/ideas.json` con todas las ideas (la confianza baja si McGonagall marcó ⚠ o si
   la idea no resiste el ataque de Voldemort).
2. Ejecuta `python3 herramientas/priorizar.py CARPETA/ideas.json`. Genera
   `CARPETA/priorizacion.md`, con la tabla ICE ordenada y la matriz impacto/esfuerzo.

## 5. Acta y cierre
1. Escribe `CARPETA/ACTA.md` con la plantilla de `conocimiento/reuniones.md` y cópiala como
   `CARPETA/RESUMEN.md`, y la versión final en `salidas/<tema>/acta_reunion.md` (con
   `priorizacion.md`).
2. Tu respuesta final empieza con `# Acta de reunión: <tema>` e incluye:
   - el reto;
   - la mejor idea de cada asistente (una línea por persona);
   - el top 3 priorizado, con su ICE;
   - la victoria rápida;
   - los riesgos ⚠ de McGonagall y los ataques de Voldemort con su defensa;
   - los siguientes pasos con el pedido sugerido.
3. Cierra **siempre** con estas dos preguntas:
   - "¿Quieres el acta también en **PPT**, como **JSON para otra IA** o con **prompts de
     imágenes**?"
   - "¿Desarrollamos alguna idea? Dime el número y la convierto en pedido."

## Reglas
- En la primera ronda nadie critica. La crítica es trabajo de McGonagall y Voldemort en la
  segunda ronda.
- Cada idea debe ser concreta: qué es, para quién y el primer paso.
- Sin cifras inventadas: una cifra sin fuente se marca como `[COMPLETAR: cifra por confirmar]`.
- La reunión no produce piezas finales. Si la persona quiere desarrollar una idea, eso es un
  pedido nuevo (con su propio briefing).
