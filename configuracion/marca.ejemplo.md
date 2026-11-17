# Marca · [COMPLETAR: nombre de tu empresa]

> **Plantilla.** Al encender el castillo por primera vez se copia como `configuracion/marca.md`
> (ese archivo es tuyo, no se sube a git). Llénalo ahí con tu manual de marca.

## Logos
Van en `oficina3d/marca/` con estos nombres (PNG con fondo transparente, unos 400–800 px de ancho):

| Archivo | Cuándo se usa |
|---|---|
| `logo_claro.png` | Sobre fondo blanco o claro (Word, PPT, piezas). Es el principal. |
| `logo_oscuro.png` | Sobre fondo oscuro o de color (portadas de PPT, encabezados). |
| `logo_una_tinta.png` | Versión a una tinta (negro), para fondos amarillos o impresión. |
| `logo_castillo.png` | El cartel del Vestíbulo en el castillo 3D (opcional). |

Si falta un logo, la PPT pone el nombre en texto, el Word sale sin logo y el castillo muestra un
letrero. En HTML se usa la ruta relativa (p. ej. `../../oficina3d/marca/logo_claro.png`); si no se
puede enlazar, se escribe `[LOGO: nombre del archivo]`.

**Reglas:** no deformar, recolorear, recortar ni poner sombras al logo; dejar aire alrededor.

## Colores
| Uso | Color |
|---|---|
| Principal | `#002F6C` `[COMPLETAR: tu color]` |
| Acento | `#FFCC00` `[COMPLETAR: tu color]` |
| Texto oscuro | `#14213D` |
| Fondo claro | `#F5F7FB` |

Los colores de la PPT y el Word se cambian en `herramientas/crear_pptx.py` y
`herramientas/crear_docx.py` (línea `AZUL, AMARILLO, TINTA, …`).

## Tipografía
- Títulos: `[COMPLETAR: p. ej. Poppins, negrita]`
- Texto: `[COMPLETAR: p. ej. Inter]`

## Tono
`[COMPLETAR: p. ej. cercano, claro y práctico; tutea al público; nada de promesas exageradas]`
