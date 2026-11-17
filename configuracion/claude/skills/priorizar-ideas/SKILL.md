---
name: priorizar-ideas
description: Prioriza una lista de ideas con puntaje ICE (impacto, confianza, facilidad) y matriz impacto/esfuerzo, y genera la tabla para el acta. Úsala al cerrar una reunión de ideas o cuando haya que elegir entre varias opciones.
---

# Priorizar ideas (ICE + matriz impacto/esfuerzo)

## 1. Arma el archivo de ideas
Crea `CARPETA/ideas.json` con una entrada por idea. Fusiona las ideas repetidas y anota a todos
sus autores:

```json
{
  "reto": "¿Cómo podríamos …?",
  "ideas": [
    {
      "id": 1,
      "titulo": "Webinar en vivo con caso real de una pyme",
      "autores": ["Harry", "Fred"],
      "descripcion": "Una línea: qué es y para quién",
      "impacto": 8,
      "confianza": 6,
      "facilidad": 7,
      "esfuerzo": "bajo",
      "riesgo": "⚠ Pedir autorización a la pyme para mostrar su caso (Ley 1581)"
    }
  ]
}
```

## 2. Cómo puntuar (de 1 a 10)
- **Impacto:** cuánto mueve el objetivo del reto. Un 10 cambia el resultado del mes.
- **Confianza:** evidencia de que funciona. Datos propios, casos, referentes o experiencia
  del equipo. Bájala si McGonagall marcó un riesgo ⚠.
- **Facilidad:** el inverso del esfuerzo. Un 10 se hace esta semana, sin presupuesto y con lo
  que hay.
- **Esfuerzo:** `bajo` si la facilidad es 7 o más, `medio` si está entre 4 y 6, y `alto` si es
  3 o menos.

Puntúa con criterio y de forma consistente entre ideas. Usa la sugerencia de confianza de
McGonagall cuando exista.

## 3. Calcula
```
python3 herramientas/priorizar.py CARPETA/ideas.json
```
Genera `CARPETA/priorizacion.md` con:
- la tabla ordenada por ICE;
- el cuadrante de cada idea (victoria rápida, apuesta grande, relleno o descartar);
- la recomendación automática del top 3.

Copia esa tabla en la sección "Priorización" del acta.

## 4. Recomienda
- **Top 3:** el ICE más alto. Si dos ideas empatan, gana la de menor esfuerzo.
- **Victoria rápida para empezar esta semana:** la de mayor facilidad entre las de impacto
  6 o más.
- **Apuesta grande:** si hay una idea de impacto 9 o 10, nómbrala aunque cueste, con su primer
  paso pequeño.
