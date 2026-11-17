"""Prioriza ideas con puntaje ICE y matriz impacto/esfuerzo.

Uso:
    python3 herramientas/priorizar.py pedidos/<carpeta>/ideas.json

Lee el JSON (esquema en .claude/skills/priorizar-ideas/SKILL.md) y escribe priorizacion.md en
la misma carpeta. Solo usa la biblioteca estándar.
"""
import json
import sys
from pathlib import Path


def nota(v):
    try:
        return max(1.0, min(10.0, float(v)))
    except (TypeError, ValueError):
        return 5.0


def cuadrante(impacto, facilidad):
    alto = impacto >= 6
    facil = facilidad >= 6
    if alto and facil:
        return "Victoria rápida"
    if alto:
        return "Apuesta grande"
    if facil:
        return "Relleno"
    return "Descartar"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(1)
    ruta = Path(sys.argv[1])
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    ideas = datos.get("ideas") or []
    if not ideas:
        raise SystemExit("El archivo no tiene ideas.")
    filas = []
    for i, idea in enumerate(ideas, 1):
        imp, conf, fac = nota(idea.get("impacto")), nota(idea.get("confianza")), nota(idea.get("facilidad"))
        ice = round((imp + conf + fac) / 3, 1)
        filas.append({**idea, "id": idea.get("id", i), "I": imp, "C": conf, "F": fac, "ICE": ice,
                      "cuadrante": cuadrante(imp, fac)})
    filas.sort(key=lambda f: (-f["ICE"], -f["F"]))

    def autores(f):
        a = f.get("autores") or []
        return ", ".join(a) if isinstance(a, list) else str(a)

    lineas = [f"# Priorización de ideas", "", f"**Reto:** {datos.get('reto', '')}", "",
              "| Puesto | # | Idea | Autor(es) | I | C | F | ICE | Cuadrante | Riesgo |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for n, f in enumerate(filas, 1):
        lineas.append(f"| {n} | {f['id']} | {f.get('titulo', '')} | {autores(f)} | {f['I']:g} | {f['C']:g} | {f['F']:g} | "
                      f"**{f['ICE']:g}** | {f['cuadrante']} | {f.get('riesgo', '') or ''} |")

    grupos = {}
    for f in filas:
        grupos.setdefault(f["cuadrante"], []).append(f)
    lineas += ["", "## Matriz impacto/esfuerzo"]
    for c in ("Victoria rápida", "Apuesta grande", "Relleno", "Descartar"):
        lineas.append(f"- **{c}:** " + ("; ".join(f"#{f['id']} {f.get('titulo', '')}" for f in grupos.get(c, [])) or "ninguna"))

    top = filas[:3]
    rapidas = [f for f in filas if f["I"] >= 6]
    rapida = max(rapidas, key=lambda f: (f["F"], f["ICE"])) if rapidas else None
    grande = next((f for f in filas if f["I"] >= 9 and f["cuadrante"] == "Apuesta grande"), None)
    lineas += ["", "## Recomendación automática (revísala antes de copiarla al acta)"]
    for n, f in enumerate(top, 1):
        lineas.append(f"{n}. **{f.get('titulo', '')}** (ICE {f['ICE']:g}, {f['cuadrante'].lower()})")
    if rapida:
        lineas.append(f"- **Para empezar esta semana:** {rapida.get('titulo', '')} (facilidad {rapida['F']:g}).")
    if grande:
        lineas.append(f"- **Apuesta grande a considerar:** {grande.get('titulo', '')} (impacto {grande['I']:g}).")

    salida = ruta.with_name("priorizacion.md")
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Listo: {salida} ({len(filas)} ideas)")


if __name__ == "__main__":
    main()
