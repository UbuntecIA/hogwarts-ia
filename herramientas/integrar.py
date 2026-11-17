"""Une las salidas finales de un pedido en un solo documento: salidas/<tema>/00_entrega_completa.md

Uso (desde la carpeta del proyecto):
    python3 herramientas/integrar.py salidas/<tema> "<Título del pedido>" [archivo1.md archivo2.md ...]

- Los archivos .md se incluyen en el orden dado (rutas relativas a la carpeta del tema o al proyecto).
  Si no se da ninguno, se toman todos los .md de la carpeta por orden alfabético, con fuentes.md al final.
- Los títulos de cada pieza bajan un nivel (# → ##) para que el documento tenga un solo título.
- Los archivos que no son texto (PPT, JSON, HTML, imágenes…) se listan al final con su enlace.
Solo usa la biblioteca estándar de Python.
"""
import datetime
import re
import sys
from pathlib import Path

SALIDA = "00_entrega_completa.md"
NOMBRES = {".pptx": "Presentación PowerPoint", ".json": "JSON para otra IA", ".html": "Página o pieza HTML",
           ".png": "Imagen", ".jpg": "Imagen", ".jpeg": "Imagen", ".svg": "Imagen", ".gift": "Quiz para Moodle (GIFT)",
           ".csv": "Datos", ".docx": "Documento Word", ".pdf": "PDF", ".txt": "Texto"}


def ancla(texto):
    t = texto.lower().strip()
    t = re.sub(r"[^\w\s-]", "", t, flags=re.UNICODE)
    return re.sub(r"\s+", "-", t)


def titulo_de(md, archivo):
    for linea in md.splitlines():
        m = re.match(r"^#\s+(.+)", linea)
        if m:
            return m.group(1).strip()
    return archivo.stem.replace("_", " ").replace("-", " ").capitalize()


def bajar_titulos(md):
    """Quita el primer título # (se usa como título de la sección) y baja un nivel los demás."""
    lineas, fuera, quitado, en_codigo = md.splitlines(), [], False, False
    for l in lineas:
        if l.strip().startswith("```"):
            en_codigo = not en_codigo
        if not en_codigo and re.match(r"^#{1,5}\s", l):
            if not quitado and re.match(r"^#\s", l):
                quitado = True
                continue
            l = "#" + l
        fuera.append(l)
    return "\n".join(fuera).strip()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    carpeta = Path(sys.argv[1])
    titulo = sys.argv[2]
    if not carpeta.is_dir():
        sys.exit(f"No existe la carpeta {carpeta}")
    pedidos = sys.argv[3:]
    if pedidos:
        archivos = []
        for a in pedidos:
            p = Path(a)
            if not p.exists():
                p = carpeta / a
            if not p.exists():
                print(f"Aviso: no encontré {a}; lo salto.")
                continue
            archivos.append(p)
    else:
        archivos = sorted(p for p in carpeta.glob("*.md") if p.name != SALIDA and p.name != "fuentes.md")
        if (carpeta / "fuentes.md").exists():
            archivos.append(carpeta / "fuentes.md")
    archivos = [p for p in archivos if p.name != SALIDA and p.suffix.lower() == ".md"]

    secciones = []
    for p in archivos:
        md = p.read_text(encoding="utf-8", errors="replace")
        secciones.append((titulo_de(md, p), p.name, bajar_titulos(md)))

    otros = sorted(p for p in carpeta.iterdir() if p.is_file() and p.suffix.lower() != ".md" and not p.name.startswith("."))
    hoy = datetime.date.today().isoformat()
    partes = [f"# {titulo}", "",
              f"**Entrega integrada** · {hoy} · Revisada por LucIA (coherencia) y ClaudIA (calidad).", "",
              "Este documento reúne todas las piezas finales del pedido en el orden en que conviene leerlas. "
              "Cada pieza también está como archivo independiente en esta misma carpeta.", "",
              "## Índice"]
    for i, (t, nombre, _) in enumerate(secciones, 1):
        partes.append(f"{i}. [{t}](#{ancla(f'{i}. {t}')}) · `{nombre}`")
    if otros:
        partes.append(f"{len(secciones) + 1}. [Archivos que no son texto](#archivos-que-no-son-texto)")
    for i, (t, nombre, cuerpo) in enumerate(secciones, 1):
        partes += ["", "---", "", f"## {i}. {t}", f"*Archivo: `{nombre}`*", "", cuerpo]
    if otros:
        partes += ["", "---", "", "## Archivos que no son texto", "", "| Archivo | Qué es |", "|---|---|"]
        for p in otros:
            partes.append(f"| [{p.name}]({p.name}) | {NOMBRES.get(p.suffix.lower(), 'Archivo')} |")
    (carpeta / SALIDA).write_text("\n".join(partes) + "\n", encoding="utf-8")
    escribir_manifiesto(carpeta, titulo)
    print(f"Listo: {carpeta / SALIDA} ({len(secciones)} piezas de texto, {len(otros)} archivos adicionales) · manifiesto.json actualizado")


def escribir_manifiesto(carpeta, titulo):
    """Inventario de la carpeta para que lo lean otros agentes (rutas relativas a la raíz del proyecto)."""
    import json
    import re as _re
    import zipfile
    raiz = carpeta.resolve().parent.parent if carpeta.resolve().parent.name == "salidas" else carpeta.resolve().parent
    archivos = []
    for p in sorted(carpeta.rglob("*")):
        if not p.is_file() or p.name.startswith(".") or p.name == "manifiesto.json":
            continue
        rel = str(p.resolve().relative_to(raiz)).replace("\\", "/")
        item = {"ruta": rel, "tipo": NOMBRES.get(p.suffix.lower(), "Texto Markdown" if p.suffix.lower() == ".md" else "Archivo"), "bytes": p.stat().st_size}
        if p.suffix.lower() == ".pptx":
            try:
                z = zipfile.ZipFile(p)
                item["diapositivas"] = len([n for n in z.namelist() if _re.match(r"ppt/slides/slide\d+\.xml", n)])
            except Exception:
                pass
        archivos.append(item)
    pendientes = []
    pj = carpeta / "prompts_imagenes.json"
    if pj.exists():
        try:
            for im in json.loads(pj.read_text(encoding="utf-8")).get("imagenes", []):
                if not (carpeta / "imagenes" / im.get("archivo", "")).exists():
                    pendientes.append({"diapositiva": im.get("diapositiva"), "archivo": im.get("archivo")})
        except ValueError:
            pass
    guion = carpeta / "presentacion.json"
    manifiesto = {"titulo": titulo, "carpeta": str(carpeta.resolve().relative_to(raiz)).replace("\\", "/") + "/",
                  "leer_primero": ["PARA_OTROS_AGENTES.md", "00_entrega_completa.md"],
                  "fuente_de_la_ppt": str(guion.resolve().relative_to(raiz)).replace("\\", "/") if guion.exists() else None,
                  "regenerar_ppt": f"python3 herramientas/crear_pptx.py {carpeta.resolve().relative_to(raiz)}/presentacion.json {carpeta.resolve().relative_to(raiz)}/presentacion.pptx".replace("\\", "/") if guion.exists() else None,
                  "imagenes_pendientes": pendientes, "archivos": archivos}
    (carpeta / "manifiesto.json").write_text(json.dumps(manifiesto, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
