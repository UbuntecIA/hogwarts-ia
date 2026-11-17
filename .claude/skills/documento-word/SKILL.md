---
name: documento-word
description: Cómo escribir un documento profesional (estrategia, campaña, documento de curso, taller, informe) en Markdown y producir su versión Word (.docx) con la marca ITERHUB usando herramientas/crear_docx.py. Úsala cuando el entregable sea un documento o la persona haya marcado "Documento Word".
---

# Documento profesional y Word

## 1. Primero el contenido, en Markdown
El documento se escribe completo en Markdown en `salidas/<tema>/<nombre>.md`. Es la versión
que se lee en la oficina 3D y la que se integra en `00_entrega_completa.md`. Reglas:
- **Portada implícita:** la primera línea es `# Título`; la segunda, una línea con subtítulo,
  cliente o programa y fecha.
- **Estructura con títulos `##` y `###`**, en el orden que diga la plantilla del tipo de
  documento (`conocimiento/marketing.md` para estrategias y campañas; skill `curso-y-taller`
  para documentos de curso y talleres).
- **Cada sección tiene contenido real:** párrafos desarrollados, tablas cuando se comparan
  cosas, listas cuando son pasos o elementos. Un título sin contenido no se deja.
- **Cifras con fuente** en el texto: (Organización, año). Bibliografía o fuentes al final.
- **`[COMPLETAR: …]`** visible donde falte un dato propio; nada de notas internas.
- Longitud de referencia: estrategia o campaña en Profesional, 8 a 15 páginas; en Experto,
  15 a 30. Documento de curso de 2 horas, 10 a 20 páginas.

## 2. Luego el Word
```
python3 herramientas/crear_docx.py salidas/<tema>/<nombre>.md salidas/<tema>/<nombre>.docx --titulo "Título" --subtitulo "Cliente o programa · fecha"
```
La herramienta crea portada con marca, encabezado con el título, pie con número de página,
títulos jerarquizados, listas, tablas con estilo, citas y saltos de página (`---` en una línea
sola). Soporta `**negrita**`, `*cursiva*` y `` `código` ``.

## 3. Verificación antes de entregar
- El `.docx` se generó sin error y pesa más de unos pocos KB.
- Los títulos siguen la jerarquía (no hay `###` sin `##` antes).
- Las tablas tienen encabezado y no superan 6 columnas (si no, se parte en dos).
- Los `[COMPLETAR]` se ven y están listados para el RESUMEN.
- El Markdown y el Word dicen lo mismo (se generó del archivo final, no de un borrador).
