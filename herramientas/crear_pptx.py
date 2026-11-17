"""Crea una presentación PowerPoint (.pptx) con la marca ITERHUB a partir de un JSON.

No necesita instalar nada: usa solo la biblioteca estándar de Python.

Uso:
    python3 herramientas/crear_pptx.py presentacion.json presentacion.pptx

Esquema del JSON: ver conocimiento/formatos.md (sección 3). "formato" puede ser "16:9"
(presentación, por defecto), "4:5" (carrusel de LinkedIn o Instagram), "1:1" o "9:16" (historias).
Tipos de diapositiva:
portada, agenda, seccion, contenido, definicion, pasos, caso, cifras, tabla, dos_columnas,
pregunta, actividad, cita, cierre; y visuales: diagrama (circulos, embudo, proceso, ciclo,
piramide), grafico (barras o columnas desde datos), iconos, linea_tiempo e imagen.
Todas aceptan "notas" (notas del presentador) y "fuente" (texto pequeño al pie).
Imágenes: una diapositiva "imagen" (o cualquier "contenido" con "imagen": "archivo.png") usa el
archivo de la carpeta imagenes/ junto al JSON; si no existe, dibuja una ilustración de marca y
deja el espacio listo para cuando la persona genere la imagen con su IA y vuelva a ejecutar
este comando.
Usa los logos de oficina3d/marca/ (logo_claro.png, logo_oscuro.png, logo_una_tinta.png) según el fondo
de cada diapositiva.
"""
import json
import struct
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
MARCA = RAIZ / "oficina3d" / "marca"
AZUL, AMARILLO, TINTA, FONDO, BLANCO, GRIS = "002F6C", "FFCC00", "14213D", "F5F7FB", "FFFFFF", "5B6578"
FUENTE_TIT, FUENTE_TXT = "Poppins", "Inter"
W, H = 12192000, 6858000
EMU = 12700  # por punto


def e(t):
    return escape(str(t if t is not None else ""), {'"': "&quot;"})


def emu(pulgadas):
    return int(pulgadas * 914400)


# ------------------------------------------------------------------ piezas de dibujo
class Diapositiva:
    def __init__(self, fondo=BLANCO):
        self.formas = []
        self.id = 2
        self.fondo = fondo
        self.imagenes = []  # (rId, ruta_media)
        self.notas = ""

    def _nid(self):
        self.id += 1
        return self.id

    def rect(self, x, y, w, h, color, redondeo=False):
        geom = "roundRect" if redondeo else "rect"
        self.formas.append(f"""<p:sp><p:nvSpPr><p:cNvPr id="{self._nid()}" name="Forma {self.id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="es-CO"/></a:p></p:txBody></p:sp>""")

    def texto(self, x, y, w, h, parrafos, ancla="t", nombre="Texto"):
        """parrafos: lista de dicts {t, tam, color, negrita, fuente, alin, vineta, espacio}."""
        ps = []
        for p in parrafos:
            alin = {"izq": "l", "centro": "ctr", "der": "r"}.get(p.get("alin", "izq"), "l")
            vineta = p.get("vineta")
            nivel = int(p.get("nivel", 0))
            margen = 342900 + nivel * 400000
            ppr = f'<a:pPr algn="{alin}"' + (f' marL="{margen}" indent="-342900"' if vineta else "") + ">"
            ppr += f'<a:spcBef><a:spcPts val="{int(p.get("espacio", 0) * 100)}"/></a:spcBef>'
            ppr += (f'<a:buClr><a:srgbClr val="{AMARILLO if not nivel else GRIS}"/></a:buClr><a:buFont typeface="Arial"/><a:buChar char="{"■" if not nivel else "–"}"/>'
                    if vineta else "<a:buNone/>")
            ppr += "</a:pPr>"
            fuente = p.get("fuente", FUENTE_TXT)
            rpr = (f'<a:rPr lang="es-CO" sz="{int(p.get("tam", 18) * 100)}" b="{1 if p.get("negrita") else 0}" dirty="0">'
                   f'<a:solidFill><a:srgbClr val="{p.get("color", TINTA)}"/></a:solidFill>'
                   f'<a:latin typeface="{fuente}"/><a:cs typeface="{fuente}"/></a:rPr>')
            ps.append(f"<a:p>{ppr}<a:r>{rpr}<a:t>{e(p['t'])}</a:t></a:r></a:p>")
        self.formas.append(f"""<p:sp><p:nvSpPr><p:cNvPr id="{self._nid()}" name="{nombre} {self.id}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{ancla}"/><a:lstStyle/>{''.join(ps)}</p:txBody></p:sp>""")

    def figura(self, prst, x, y, w, h, color, alfa=None, linea=None, rot=0):
        """Forma geométrica: ellipse, triangle, rightArrow, chevron, homePlate, roundRect, trapezoid, diamond…"""
        alfa_xml = '<a:alpha val="%d"/>' % int(alfa * 1000) if alfa is not None else ""
        relleno = f'<a:solidFill><a:srgbClr val="{color}">{alfa_xml}</a:srgbClr></a:solidFill>' if color else "<a:noFill/>"
        ln = f'<a:ln w="{int(linea[1] * EMU)}"><a:solidFill><a:srgbClr val="{linea[0]}"/></a:solidFill></a:ln>' if linea else "<a:ln><a:noFill/></a:ln>"
        self.formas.append(f"""<p:sp><p:nvSpPr><p:cNvPr id="{self._nid()}" name="Figura {self.id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm rot="{int(rot * 60000)}"><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>{relleno}{ln}</p:spPr>
<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="es-CO"/></a:p></p:txBody></p:sp>""")

    def imagen(self, rid, x, y, w, h):
        self.formas.append(f"""<p:pic><p:nvPicPr><p:cNvPr id="{self._nid()}" name="Logo {self.id}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>""")

    def xml(self):
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{self.fondo}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
{''.join(self.formas)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"""


def tam_png(ruta):
    with open(ruta, "rb") as f:
        cab = f.read(24)
    if cab[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", cab[16:24])


def tam_imagen(ruta):
    """Ancho y alto en píxeles de un PNG o JPEG."""
    t = tam_png(ruta)
    if t:
        return t
    try:
        with open(ruta, "rb") as f:
            datos = f.read()
    except OSError:
        return None
    if datos[:2] != b"\xff\xd8":
        return None
    i = 2
    while i < len(datos) - 9:
        if datos[i] != 0xFF:
            i += 1
            continue
        marca = datos[i + 1]
        if marca in (0xC0, 0xC1, 0xC2):
            alto, ancho = struct.unpack(">HH", datos[i + 5:i + 9])
            return ancho, alto
        i += 2 + struct.unpack(">H", datos[i + 2:i + 4])[0]
    return None


CARPETA_JSON = Path(".")


def buscar_imagen(nombre):
    """Busca la imagen de una diapositiva: ruta tal cual, o en imagenes/ junto al JSON."""
    if not nombre:
        return None
    candidatos = [Path(nombre), CARPETA_JSON / nombre, CARPETA_JSON / "imagenes" / nombre, CARPETA_JSON / "imagenes" / Path(nombre).name]
    for c in candidatos:
        if c.is_file() and tam_imagen(c):
            return c
    return None


def poner_imagen(d, medios, ruta, x, y, w, h):
    """Inserta una imagen ajustada dentro del recuadro (sin deformar, centrada)."""
    ancho_px, alto_px = tam_imagen(ruta)
    esc = min(w / ancho_px, h / alto_px)
    aw, ah = int(ancho_px * esc), int(alto_px * esc)
    if ruta not in medios:
        medios[ruta] = f"img{len(medios) + 1}{ruta.suffix.lower()}"
    rid = f"rIdImg{len(d.imagenes) + 1}"
    d.imagenes.append((rid, medios[ruta]))
    d.imagen(rid, x + (w - aw) // 2, y + (h - ah) // 2, aw, ah)


def ilustracion(d, x, y, w, h, semilla=0):
    """Ilustración abstracta de marca (círculos y barras) para cuando aún no hay imagen."""
    d.rect(x, y, w, h, FONDO, redondeo=True)
    k = (semilla % 4)
    formas = [("ellipse", 0.55, 0.05, 0.5, AZUL, 18), ("ellipse", 0.05, 0.35, 0.42, AMARILLO, 40), ("ellipse", 0.62, 0.5, 0.32, "2E5BBA", 25),
              ("roundRect", 0.18, 0.12, 0.25, "2B7A78", 22), ("ellipse", 0.38, 0.55, 0.2, AMARILLO, 60), ("roundRect", 0.72, 0.18, 0.18, AZUL, 30)]
    for i, (prst, fx, fy, fw, color, alfa) in enumerate(formas):
        fx, fy = ((fx + 0.15 * k) % 0.75, (fy + 0.1 * k) % 0.7)
        d.figura(prst, x + int(w * fx), y + int(h * fy), int(w * fw), int(h * fw * (0.75 if prst == "roundRect" else 1)), color, alfa=alfa)


def buscar_logo(fondo):
    """fondo: 'oscuro' (azul), 'claro' (blanco) o 'amarillo'. Logos de oficina3d/marca/ (ver su LEEME.md)."""
    nombres = {"oscuro": ["logo_oscuro.png"],
               "claro": ["logo_claro.png", "logo_una_tinta.png"],
               "amarillo": ["logo_una_tinta.png", "logo_claro.png"]}[fondo]
    for n in nombres:
        p = MARCA / n
        if p.exists() and tam_png(p):
            return p
    return None


# ------------------------------------------------------------------ diseño por tipo
def marca_texto(d, x, y, oscuro, tam=20, acento=AMARILLO):
    """Logo en texto (cuando no hay archivo): ITER en blanco o azul y HUB en amarillo."""
    color = BLANCO if oscuro else AZUL
    d.formas.append(f"""<p:sp><p:nvSpPr><p:cNvPr id="{d._nid()}" name="Marca {d.id}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{emu(2.4)}" cy="{emu(0.45)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/><a:lstStyle/><a:p>
<a:r><a:rPr lang="es-CO" sz="{tam * 100}" b="1"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{FUENTE_TIT}"/></a:rPr><a:t>ITER</a:t></a:r>
<a:r><a:rPr lang="es-CO" sz="{tam * 100}" b="1"><a:solidFill><a:srgbClr val="{acento}"/></a:solidFill><a:latin typeface="{FUENTE_TIT}"/></a:rPr><a:t>HUB</a:t></a:r>
</a:p></p:txBody></p:sp>""")


def poner_logo(d, medios, oscuro, x, y, alto, acento=AMARILLO, fondo=None):
    ruta = buscar_logo(fondo or ("oscuro" if oscuro else "claro"))
    if not ruta:
        marca_texto(d, x, y, oscuro, tam=max(11, int(alto / EMU * 0.6)), acento=acento)
        return
    ancho_px, alto_px = tam_png(ruta)
    ancho = int(alto * ancho_px / alto_px)
    if ruta not in medios:
        medios[ruta] = f"logo{len(medios) + 1}.png"
    rid = f"rIdImg{len(d.imagenes) + 1}"
    d.imagenes.append((rid, medios[ruta]))
    d.imagen(rid, x, y, ancho, alto)


FORMATOS = {"16:9": (13.333, 7.5), "4:5": (7.5, 9.375), "1:1": (7.5, 7.5), "9:16": (7.5, 13.333)}


def usar_formato(formato):
    """Cambia el tamaño de diapositiva. Las posiciones se escalan desde un diseño base de 13,333 × 7,5 pulgadas."""
    global W, H
    ancho, alto = FORMATOS.get(str(formato or "16:9"), FORMATOS["16:9"])
    W, H = emu(ancho), emu(alto)


def X(pulg):
    return int(W * pulg / 13.333)


def Y(pulg):
    return int(H * pulg / 7.5)


def vertical():
    return H > W


def pie(d, medios, n, total):
    d.rect(X(0.6), H - Y(0.55), X(0.5), Y(0.06), AMARILLO)
    d.texto(W - X(1.6), H - Y(0.62), X(1.0), Y(0.3), [{"t": f"{n} / {total}", "tam": 10, "color": GRIS, "alin": "der"}])
    poner_logo(d, medios, False, W - X(3.3), H - Y(0.7), emu(0.32), acento=TINTA)


def titulo_contenido(d, titulo):
    d.rect(0, 0, emu(0.18), Y(1.45), AMARILLO)
    d.texto(X(0.6), Y(0.45), W - X(1.2), Y(0.9),
            [{"t": titulo, "tam": 30, "negrita": True, "color": AZUL, "fuente": FUENTE_TIT}], ancla="ctr", nombre="Título")


def vinetas(puntos, tam=20):
    """puntos: textos o dicts {"t": "...", "sub": ["..."]}; los subpuntos van en un nivel menor."""
    salida = []
    for p in puntos:
        if isinstance(p, dict):
            salida.append({"t": p.get("t", ""), "tam": tam, "vineta": True, "espacio": 8, "color": TINTA})
            for q in p.get("sub") or []:
                salida.append({"t": q, "tam": max(12, tam - 4), "vineta": True, "nivel": 1, "espacio": 2, "color": GRIS})
        else:
            salida.append({"t": p, "tam": tam, "vineta": True, "espacio": 8, "color": TINTA})
    return salida


def tam_auto(textos, base, minimo=14):
    """Baja el tamaño de letra cuando hay mucho texto, para que no se desborde."""
    n = sum(len(str(t)) for t in textos)
    if n > 900:
        return max(minimo, base - 8)
    if n > 600:
        return max(minimo, base - 5)
    if n > 380:
        return max(minimo, base - 3)
    return base


def nota_fuente(d, s):
    if s.get("fuente"):
        d.texto(X(0.6), H - Y(0.95), W - X(1.2), Y(0.32), [{"t": "Fuente: " + str(s["fuente"]), "tam": 10, "color": GRIS}], ancla="b")


def tarjeta(d, x, y, w, h, titulo, texto, color=AZUL, tam_t=16, tam_x=14):
    d.rect(x, y, w, h, FONDO, redondeo=True)
    d.rect(x, y, emu(0.07), h, color)
    d.texto(x + emu(0.22), y + emu(0.14), w - emu(0.35), emu(0.4), [{"t": titulo, "tam": tam_t, "negrita": True, "color": color, "fuente": FUENTE_TIT}])
    d.texto(x + emu(0.22), y + emu(0.55), w - emu(0.35), h - emu(0.65), [{"t": texto, "tam": tam_x, "color": TINTA}])


def construir(s, medios, n, total):
    tipo = s.get("tipo", "contenido")
    if tipo in ("portada", "cierre"):
        d = Diapositiva(AZUL)
        d.figura("ellipse", W - X(4.2), -Y(1.6), X(5.6), X(5.6), "2E5BBA", alfa=45)
        d.figura("ellipse", W - X(2.6), Y(3.2), X(3.4), X(3.4), AMARILLO, alfa=22)
        d.figura("ellipse", W - X(5.0), Y(4.6), X(1.3), X(1.3), AMARILLO, alfa=70)
        foto = buscar_imagen(s.get("imagen"))
        if foto:
            d.figura("roundRect", W - X(5.6), Y(1.2), X(4.6), Y(4.4), BLANCO)
            poner_imagen(d, medios, foto, W - X(5.5), Y(1.3), X(4.4), Y(4.2))
        d.rect(0, H - Y(0.35), W, Y(0.35), AMARILLO)
        d.rect(X(0.8), Y(2.55), emu(1.2), emu(0.1), AMARILLO)
        poner_logo(d, medios, True, X(0.8), Y(0.6), emu(0.6))
        ancho_t = W - X(7.0) if foto else W - X(4.2)
        titulo = s.get("titulo", "")
        tam_t = 44 if tipo == "portada" else 48
        if len(titulo) > 70:
            tam_t = 30
        elif len(titulo) > 45:
            tam_t = 36
        d.texto(X(0.8), Y(2.2), ancho_t, Y(2.75),
                [{"t": titulo, "tam": tam_t, "negrita": True, "color": BLANCO, "fuente": FUENTE_TIT}], ancla="b", nombre="Título")
        if s.get("subtitulo"):
            d.texto(X(0.8), Y(5.1), ancho_t, Y(0.9), [{"t": s["subtitulo"], "tam": 18, "color": AMARILLO}])
    elif tipo == "seccion":
        d = Diapositiva(AMARILLO)
        d.figura("ellipse", W - X(3.6), Y(-1.2), X(4.8), X(4.8), AZUL, alfa=12)
        d.figura("ellipse", W - X(1.8), Y(4.2), X(2.6), X(2.6), BLANCO, alfa=35)
        if s.get("numero") or s.get("n"):
            d.texto(W - X(3.2), Y(0.25), X(2.4), Y(1.8), [{"t": str(s.get("numero") or s.get("n")), "tam": 96, "negrita": True, "color": AZUL, "fuente": FUENTE_TIT, "alin": "der"}], ancla="ctr")
        d.texto(X(0.8), Y(2.3), W - X(1.6), Y(1.4),
                [{"t": s.get("titulo", ""), "tam": 44, "negrita": True, "color": AZUL, "fuente": FUENTE_TIT}], ancla="b", nombre="Título")
        d.rect(X(0.8), Y(3.85), emu(1.2), emu(0.1), AZUL)
        if s.get("subtitulo"):
            d.texto(X(0.8), Y(4.1), W - X(1.6), Y(0.8), [{"t": s["subtitulo"], "tam": 22, "color": TINTA}])
        poner_logo(d, medios, False, X(0.8), Y(0.6), emu(0.45), acento=TINTA, fondo="amarillo")
    elif tipo == "cita":
        d = Diapositiva(AZUL)
        d.texto(X(1.0), Y(0.8), emu(2), emu(1.5), [{"t": "“", "tam": 120, "color": AMARILLO, "fuente": FUENTE_TIT, "negrita": True}])
        d.texto(X(1.4), Y(2.0), W - X(2.8), Y(2.6),
                [{"t": s.get("texto", ""), "tam": 30, "color": BLANCO, "fuente": FUENTE_TIT}], ancla="ctr")
        if s.get("autor"):
            d.texto(X(1.4), Y(4.9), W - X(2.8), Y(0.6), [{"t": "— " + s["autor"], "tam": 18, "color": AMARILLO, "negrita": True}])
    elif tipo == "dos_columnas":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        for i, lado in enumerate(("izquierda", "derecha")):
            c = s.get(lado, {}) or {}
            if vertical():  # una columna debajo de la otra
                x, ancho = X(0.6), W - X(1.2)
                alto = (Y(5.95) - Y(1.7) - Y(0.2)) // 2
                y = Y(1.7) + i * (alto + Y(0.2))
            else:
                ancho = (W - X(1.2) - X(0.4)) // 2
                x, y, alto = X(0.6) + i * (ancho + X(0.4)), Y(1.7), Y(4.3)
            d.rect(x, y, ancho, alto, FONDO, redondeo=True)
            d.rect(x, y, ancho, emu(0.08), AZUL if i == 0 else AMARILLO)
            d.texto(x + emu(0.3), y + emu(0.25), ancho - emu(0.6), emu(0.55),
                    [{"t": c.get("titulo", ""), "tam": 22, "negrita": True, "color": AZUL, "fuente": FUENTE_TIT}])
            d.texto(x + emu(0.3), y + emu(0.9), ancho - emu(0.6), alto - emu(1.1), vinetas(c.get("puntos", []), tam_auto(c.get("puntos", []), 18)))
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "cifras":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        cifras = (s.get("cifras") or [])[:4]
        k = max(1, len(cifras))
        for i, c in enumerate(cifras):
            if vertical():  # una cifra por fila
                x, ancho = X(0.6), W - X(1.2)
                alto = (Y(5.9) - Y(1.8) - Y(0.15) * (k - 1)) // k
                y = Y(1.8) + i * (alto + Y(0.15))
                d.rect(x, y, ancho, alto, FONDO, redondeo=True)
                d.texto(x + emu(0.3), y, emu(2.4), alto,
                        [{"t": c.get("valor", ""), "tam": 40, "negrita": True, "color": AZUL, "fuente": FUENTE_TIT}], ancla="ctr")
                d.texto(x + emu(2.8), y, ancho - emu(3.0), alto, [{"t": c.get("texto", ""), "tam": 18, "color": TINTA}], ancla="ctr")
                continue
            ancho = (W - X(1.2) - X(0.3) * (k - 1)) // k
            x = X(0.6) + i * (ancho + X(0.3))
            d.rect(x, Y(2.0), ancho, Y(3.2), FONDO, redondeo=True)
            d.texto(x + emu(0.2), Y(2.3), ancho - emu(0.4), Y(1.3),
                    [{"t": c.get("valor", ""), "tam": 54, "negrita": True, "color": AZUL, "fuente": FUENTE_TIT, "alin": "centro"}], ancla="ctr")
            d.rect(x + ancho // 2 - emu(0.4), Y(3.7), emu(0.8), emu(0.07), AMARILLO)
            d.texto(x + emu(0.25), Y(3.95), ancho - emu(0.5), Y(1.3), [{"t": c.get("texto", ""), "tam": 16, "color": TINTA, "alin": "centro"}])
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "agenda":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", "Agenda"))
        bloques = (s.get("bloques") or [])[:8]
        alto = min(Y(0.62), (Y(5.9) - Y(1.75)) // max(1, len(bloques)))
        for i, b in enumerate(bloques):
            y = Y(1.75) + i * alto
            d.rect(X(0.8), y + emu(0.06), emu(0.5), alto - emu(0.12), AMARILLO, redondeo=True)
            d.texto(X(0.8), y + emu(0.06), emu(0.5), alto - emu(0.12), [{"t": str(i + 1), "tam": 18, "negrita": True, "color": AZUL, "alin": "centro", "fuente": FUENTE_TIT}], ancla="ctr")
            d.texto(X(1.5), y, W - X(3.6), alto, [{"t": b.get("titulo", ""), "tam": 20, "color": TINTA}], ancla="ctr")
            d.texto(W - X(2.2), y, X(1.6), alto, [{"t": b.get("tiempo", ""), "tam": 16, "color": GRIS, "alin": "der"}], ancla="ctr")
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "definicion":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("termino") or s.get("titulo", ""))
        d.rect(X(0.8), Y(1.8), W - X(1.6), Y(1.9), FONDO, redondeo=True)
        d.rect(X(0.8), Y(1.8), emu(0.08), Y(1.9), AZUL)
        d.texto(X(1.1), Y(1.95), W - X(2.2), Y(1.6), [{"t": s.get("definicion", ""), "tam": tam_auto([s.get("definicion", "")], 22), "color": TINTA}], ancla="ctr")
        if s.get("ejemplo"):
            d.texto(X(0.8), Y(3.95), emu(1.6), Y(0.45), [{"t": "Ejemplo", "tam": 14, "negrita": True, "color": AZUL, "fuente": FUENTE_TIT}])
            d.texto(X(0.8), Y(4.4), W - X(1.6), Y(1.5), [{"t": s["ejemplo"], "tam": tam_auto([s["ejemplo"]], 18), "color": TINTA}])
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "pasos":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        pasos = (s.get("pasos") or [])[:6]
        k = max(1, len(pasos))
        if vertical() or k > 3:   # dos filas
            filas, cols = (2, (k + 1) // 2) if not vertical() else (k, 1)
        else:
            filas, cols = 1, k
        ancho = (W - X(1.2) - X(0.25) * (cols - 1)) // cols
        alto = (Y(5.95) - Y(1.75) - Y(0.2) * (filas - 1)) // filas
        tam_x = 13 if k > 4 else 15
        for i, ps in enumerate(pasos):
            x = X(0.6) + (i % cols) * (ancho + X(0.25))
            y = Y(1.75) + (i // cols) * (alto + Y(0.2))
            d.rect(x, y, ancho, alto, FONDO, redondeo=True)
            d.rect(x + emu(0.2), y + emu(0.18), emu(0.42), emu(0.42), AMARILLO, redondeo=True)
            d.texto(x + emu(0.2), y + emu(0.18), emu(0.42), emu(0.42), [{"t": str(i + 1), "tam": 16, "negrita": True, "color": AZUL, "alin": "centro", "fuente": FUENTE_TIT}], ancla="ctr")
            d.texto(x + emu(0.72), y + emu(0.18), ancho - emu(0.9), emu(0.5), [{"t": ps.get("titulo", ""), "tam": 15, "negrita": True, "color": AZUL, "fuente": FUENTE_TIT}], ancla="ctr")
            d.texto(x + emu(0.2), y + emu(0.75), ancho - emu(0.4), alto - emu(0.9), [{"t": ps.get("texto", ""), "tam": tam_x, "color": TINTA}])
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "caso":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, "Caso: " + str(s.get("empresa", s.get("titulo", ""))))
        ancho = (W - X(1.2) - X(0.25)) // 2
        alto = (Y(5.95) - Y(1.75) - Y(0.2)) // 2
        celdas = [("Contexto", s.get("contexto", ""), AZUL), ("Qué hizo", s.get("accion", ""), AZUL),
                  ("Resultado", s.get("resultado", ""), "2B7A78"), ("Lo que enseña", s.get("leccion", ""), "B45309")]
        if vertical():
            ancho, alto = W - X(1.2), (Y(5.95) - Y(1.75) - Y(0.15) * 3) // 4
        for i, (t, x_, c) in enumerate(celdas):
            x = X(0.6) + (0 if vertical() else (i % 2) * (ancho + X(0.25)))
            y = Y(1.75) + (i if vertical() else i // 2) * (alto + (Y(0.15) if vertical() else Y(0.2)))
            tarjeta(d, x, y, ancho, alto, t, x_, c, 15, tam_auto([x_], 14, 11))
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "tabla":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        cols = [str(c) for c in (s.get("columnas") or [])][:6]
        filas = [[str(c) for c in f][:len(cols)] for f in (s.get("filas") or [])][:8]
        if cols:
            ancho = (W - X(1.2)) // len(cols)
            alto = min(Y(0.6), (Y(5.95) - Y(1.75)) // (len(filas) + 1))
            tam = 12 if len(cols) > 4 or len(filas) > 5 else 14
            for j, c in enumerate(cols):
                d.rect(X(0.6) + j * ancho, Y(1.75), ancho - emu(0.03), alto, AZUL)
                d.texto(X(0.6) + j * ancho + emu(0.1), Y(1.75), ancho - emu(0.2), alto, [{"t": c, "tam": tam, "negrita": True, "color": BLANCO}], ancla="ctr")
            for i, f in enumerate(filas):
                y = Y(1.75) + (i + 1) * alto
                for j in range(len(cols)):
                    d.rect(X(0.6) + j * ancho, y, ancho - emu(0.03), alto - emu(0.03), FONDO if i % 2 == 0 else BLANCO)
                    d.texto(X(0.6) + j * ancho + emu(0.1), y, ancho - emu(0.2), alto, [{"t": f[j] if j < len(f) else "", "tam": tam, "color": TINTA, "negrita": j == 0}], ancla="ctr")
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "pregunta":
        d = Diapositiva(AZUL)
        d.rect(0, H - Y(0.35), W, Y(0.35), AMARILLO)
        d.texto(X(1.0), Y(0.7), emu(2), emu(1.2), [{"t": "?", "tam": 110, "color": AMARILLO, "fuente": FUENTE_TIT, "negrita": True}])
        d.texto(X(1.2), Y(1.9), W - X(2.4), Y(2.4), [{"t": s.get("texto", s.get("titulo", "")), "tam": tam_auto([s.get("texto", "")], 34, 22), "color": BLANCO, "fuente": FUENTE_TIT, "negrita": True}], ancla="ctr")
        pistas = s.get("pistas") or []
        if pistas:
            d.texto(X(1.2), Y(4.5), W - X(2.4), Y(1.6), [{"t": "Pistas", "tam": 14, "negrita": True, "color": AMARILLO}] + [{"t": p_, "tam": 16, "color": BLANCO, "vineta": True, "espacio": 4} for p_ in pistas[:4]])
        poner_logo(d, medios, True, W - X(3.0), H - Y(0.95), emu(0.32))
    elif tipo == "actividad":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", "Actividad"))
        d.rect(X(0.6), Y(1.75), W - X(1.2), Y(0.5), AMARILLO, redondeo=True)
        d.texto(X(0.8), Y(1.75), W - X(1.6), Y(0.5), [{"t": f"⏱ {s.get('tiempo', '')}   ·   Entregable: {s.get('entregable', '')}", "tam": 14, "negrita": True, "color": AZUL}], ancla="ctr")
        instr = s.get("instrucciones") or []
        d.texto(X(0.8), Y(2.45), W - X(1.6), Y(3.4), [{"t": f"{i + 1}. {t}", "tam": tam_auto(instr, 18), "color": TINTA, "espacio": 8} for i, t in enumerate(instr[:7])])
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "imagen":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        foto = buscar_imagen(s.get("archivo") or s.get("imagen"))
        texto = s.get("texto") or ""
        if texto:   # imagen a la izquierda, texto a la derecha
            ax, aw = X(0.6), (W - X(1.2)) * 55 // 100
            tx, tw = ax + aw + X(0.3), W - X(1.2) - aw - X(0.3)
            d.texto(tx, Y(1.85), tw, Y(3.6), [{"t": texto, "tam": tam_auto([texto], 18), "color": TINTA}])
        else:
            ax, aw = X(0.6), W - X(1.2)
        if foto:
            poner_imagen(d, medios, foto, ax, Y(1.75), aw, Y(3.6))
        else:
            ilustracion(d, ax, Y(1.75), aw, Y(3.6), n)
            d.rect(ax + emu(0.3), Y(4.55), aw - emu(0.6), Y(0.7), BLANCO, redondeo=True)
            d.texto(ax + emu(0.45), Y(4.55), aw - emu(0.9), Y(0.7), [{"t": "Imagen por generar: " + str(s.get("descripcion", ""))[:160] + " · prompt en prompts_imagenes.md", "tam": 10, "color": GRIS}], ancla="ctr")
        if s.get("pie"):
            d.texto(X(0.6), Y(5.45), W - X(1.2), Y(0.5), [{"t": s["pie"], "tam": 14, "color": TINTA, "alin": "centro"}])
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "diagrama":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        sub = s.get("subtipo", "proceso")
        items = s.get("items") or s.get("niveles") or s.get("pasos") or []
        items = [(it if isinstance(it, dict) else {"titulo": str(it)}) for it in items][:6]
        colores = [AZUL, "2E5BBA", "2B7A78", "B45309", "8E44AD", GRIS]
        cx, cy = W // 2, Y(1.75) + (Y(5.95) - Y(1.75)) // 2
        if sub == "circulos":   # concéntricos: el primero es el mayor (TAM) y el último el menor (SOM)
            k = len(items)
            rmax = min(Y(4.1), X(4.1)) // 2
            for i, it in enumerate(items):
                r = int(rmax * (1 - i / max(k, 1) * 0.72))
                d.figura("ellipse", cx - X(2.2) - r, cy - r, 2 * r, 2 * r, colores[i % len(colores)], alfa=35 + i * 15)
            for i, it in enumerate(items):
                r = int(rmax * (1 - i / max(k, 1) * 0.72))
                d.texto(cx - X(2.2) - r, cy - r - Y(0.05) + (0 if i else -Y(0.3)), 2 * r, Y(0.4), [{"t": it.get("titulo", ""), "tam": 14, "negrita": True, "color": BLANCO if i else AZUL, "alin": "centro"}])
            for i, it in enumerate(items):
                y = Y(1.9) + i * ((Y(5.9) - Y(1.9)) // max(k, 1))
                tarjeta(d, cx + X(2.3), y, X(4.0), (Y(5.9) - Y(1.9)) // max(k, 1) - Y(0.15), it.get("titulo", ""), it.get("texto", ""), colores[i % len(colores)], 14, 12)
        elif sub == "embudo" or sub == "piramide":
            k = len(items)
            alto = (Y(5.95) - Y(1.75) - Y(0.08) * (k - 1)) // max(k, 1)
            for i, it in enumerate(items):
                frac = (1 - i / max(k, 1) * 0.6) if sub == "embudo" else (0.4 + i / max(k, 1) * 0.6)
                ancho = int(X(6.0) * frac)
                y = Y(1.75) + i * (alto + Y(0.08))
                d.figura("roundRect" if sub == "piramide" else "trapezoid", cx - X(2.6) - ancho // 2, y, ancho, alto, colores[i % len(colores)], rot=180 if sub == "embudo" else 0)
                d.texto(cx - X(2.6) - ancho // 2, y, ancho, alto, [{"t": it.get("titulo", ""), "tam": 14, "negrita": True, "color": BLANCO, "alin": "centro"}], ancla="ctr")
                d.texto(cx + X(1.0), y, X(4.8), alto, [{"t": it.get("texto", ""), "tam": tam_auto([it.get("texto", "")], 13, 10), "color": TINTA}], ancla="ctr")
        elif sub == "ciclo":
            k = len(items)
            import math
            R = min(Y(1.75), X(2.3))
            for i, it in enumerate(items):
                a = -math.pi / 2 + 2 * math.pi * i / max(k, 1)
                bx, by = cx + int(R * math.cos(a)), cy + int(R * math.sin(a))
                d.figura("ellipse", bx - X(0.9), by - Y(0.5), X(1.8), Y(1.0), colores[i % len(colores)])
                d.texto(bx - X(0.9), by - Y(0.5), X(1.8), Y(1.0), [{"t": it.get("titulo", ""), "tam": 12, "negrita": True, "color": BLANCO, "alin": "centro"}], ancla="ctr")
                if it.get("texto"):
                    lx = bx + (X(1.0) if math.cos(a) >= 0 else -X(3.6))
                    d.texto(lx, by - Y(0.45) + (Y(0.55) if math.sin(a) > 0.5 else -Y(0.55) if math.sin(a) < -0.5 else 0), X(2.6), Y(0.9), [{"t": it["texto"], "tam": 10, "color": GRIS, "alin": "izq" if math.cos(a) >= 0 else "der"}], ancla="ctr")
            d.figura("ellipse", cx - X(0.6), cy - Y(0.6), X(1.2), Y(1.2), AMARILLO, alfa=60)
        else:   # proceso: cajas con flechas
            k = len(items)
            gap = X(0.35)
            ancho = (W - X(1.2) - gap * (k - 1)) // max(k, 1)
            for i, it in enumerate(items):
                x = X(0.6) + i * (ancho + gap)
                d.figura("homePlate" if i < k - 1 else "roundRect", x, Y(2.1), ancho, Y(1.1), colores[i % len(colores)])
                d.texto(x + emu(0.1), Y(2.1), ancho - emu(0.3), Y(1.1), [{"t": f"{i + 1}. {it.get('titulo', '')}", "tam": 13 if k > 4 else 15, "negrita": True, "color": BLANCO, "alin": "centro"}], ancla="ctr")
                d.texto(x, Y(3.4), ancho, Y(2.5), [{"t": it.get("texto", ""), "tam": tam_auto([it.get("texto", "")], 13, 10), "color": TINTA}])
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "grafico":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        serie = [(str(q.get("etiqueta", "")), float(q.get("valor", 0) or 0), str(q.get("texto", q.get("valor", "")))) for q in (s.get("series") or s.get("datos") or [])][:8]
        maximo = max([v for _, v, _ in serie] + [1])
        if s.get("subtipo", "barras") == "columnas" and not vertical():
            k = len(serie)
            ancho = (W - X(1.6)) // max(k, 1)
            base = Y(5.3)
            for i, (et, v, txt) in enumerate(serie):
                h = int(Y(3.2) * v / maximo)
                x = X(0.8) + i * ancho
                d.rect(x + ancho // 5, base - h, ancho * 3 // 5, h, AZUL if i != serie.index(max(serie, key=lambda q: q[1])) else AMARILLO, redondeo=True)
                d.texto(x, base - h - Y(0.4), ancho, Y(0.35), [{"t": txt, "tam": 12, "negrita": True, "color": TINTA, "alin": "centro"}])
                d.texto(x, base + Y(0.05), ancho, Y(0.6), [{"t": et, "tam": 11, "color": GRIS, "alin": "centro"}])
            d.rect(X(0.8), base, W - X(1.6), emu(0.02), GRIS)
        else:
            k = len(serie)
            alto = (Y(5.8) - Y(1.75)) // max(k, 1)
            for i, (et, v, txt) in enumerate(serie):
                y = Y(1.75) + i * alto
                d.texto(X(0.6), y, X(3.2), alto - Y(0.1), [{"t": et, "tam": 12, "color": TINTA, "alin": "der"}], ancla="ctr")
                wbar = int((W - X(6.2)) * v / maximo)
                d.rect(X(4.0), y + alto // 4, max(wbar, emu(0.05)), alto // 2, AZUL if v != maximo else AMARILLO, redondeo=True)
                d.texto(X(4.0) + wbar + X(0.15), y, X(2.0), alto - Y(0.1), [{"t": txt, "tam": 12, "negrita": True, "color": TINTA}], ancla="ctr")
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "iconos":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        items = (s.get("items") or [])[:4]
        k = len(items)
        gap = X(0.3)
        ancho = (W - X(1.2) - gap * (k - 1)) // max(k, 1)
        for i, it in enumerate(items):
            x = X(0.6) + i * (ancho + gap)
            d.rect(x, Y(1.75), ancho, Y(4.2), FONDO, redondeo=True)
            d.figura("ellipse", x + ancho // 2 - X(0.55), Y(2.0), X(1.1), X(1.1), AMARILLO)
            d.texto(x + ancho // 2 - X(0.55), Y(2.0), X(1.1), X(1.1), [{"t": str(it.get("icono", "") or (it.get("titulo", "?")[:1])), "tam": 30, "color": AZUL, "alin": "centro", "negrita": True}], ancla="ctr")
            d.texto(x + emu(0.2), Y(3.35), ancho - emu(0.4), Y(0.6), [{"t": it.get("titulo", ""), "tam": 15, "negrita": True, "color": AZUL, "alin": "centro", "fuente": FUENTE_TIT}], ancla="ctr")
            d.texto(x + emu(0.2), Y(4.0), ancho - emu(0.4), Y(1.9), [{"t": it.get("texto", ""), "tam": tam_auto([it.get("texto", "")], 13, 10), "color": TINTA, "alin": "centro"}])
        nota_fuente(d, s)
        pie(d, medios, n, total)
    elif tipo == "linea_tiempo":
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        hitos = (s.get("hitos") or [])[:6]
        k = len(hitos)
        d.rect(X(0.8), Y(3.3), W - X(1.6), emu(0.06), AZUL)
        paso = (W - X(1.6)) // max(k, 1)
        for i, h in enumerate(hitos):
            x = X(0.8) + i * paso + paso // 2
            d.figura("ellipse", x - X(0.22), Y(3.3) - Y(0.2), X(0.44), X(0.44), AMARILLO, linea=(AZUL, 2))
            arriba = i % 2 == 0
            d.texto(x - paso // 2 + emu(0.1), Y(1.8) if arriba else Y(3.75), paso - emu(0.2), Y(0.45), [{"t": str(h.get("fecha", "")), "tam": 13, "negrita": True, "color": AZUL, "alin": "centro", "fuente": FUENTE_TIT}], ancla="b" if arriba else "t")
            d.texto(x - paso // 2 + emu(0.1), Y(2.25) if arriba else Y(4.2), paso - emu(0.2), Y(0.95) if arriba else Y(1.6), [{"t": str(h.get("texto", "")), "tam": tam_auto([h.get("texto", "")], 11, 9), "color": TINTA, "alin": "centro"}], ancla="b" if arriba else "t")
        nota_fuente(d, s)
        pie(d, medios, n, total)
    else:  # contenido
        d = Diapositiva(BLANCO)
        titulo_contenido(d, s.get("titulo", ""))
        puntos = s.get("puntos") or []
        texto = s.get("texto", "")
        todos = [texto] + [q.get("t", "") + " ".join(q.get("sub") or []) if isinstance(q, dict) else q for q in puntos]
        tam = tam_auto(todos, 22 if len(puntos) <= 4 else 20)
        y0 = Y(1.8)
        foto = buscar_imagen(s.get("imagen"))
        ancho_txt = W - X(1.6)
        if foto or s.get("imagen"):
            ancho_txt = (W - X(1.6)) * 58 // 100
            ix, iw = X(0.8) + ancho_txt + X(0.3), W - X(1.1) - ancho_txt - X(0.3)
            if foto:
                poner_imagen(d, medios, foto, ix, Y(1.8), iw, Y(4.0))
            else:
                ilustracion(d, ix, Y(1.8), iw, Y(4.0), n)
            tam = tam_auto(todos, 18)
        if texto:
            alto_txt = Y(0.5) + Y(0.32) * (len(texto) * (W - X(1.6)) // ancho_txt // 95)
            d.texto(X(0.8), y0, ancho_txt, alto_txt, [{"t": texto, "tam": tam, "color": TINTA}])
            y0 += alto_txt + Y(0.15)
        if puntos:
            d.texto(X(0.8), y0, ancho_txt, Y(6.0) - y0, vinetas(puntos, tam))
        nota_fuente(d, s)
        pie(d, medios, n, total)
    d.notas = s.get("notas", "")
    return d


# ------------------------------------------------------------------ partes fijas del paquete
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CABEZA = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

TEMA = CABEZA + f"""<a:theme xmlns:a="{NS_A}" name="ITERHUB"><a:themeElements>
<a:clrScheme name="ITERHUB"><a:dk1><a:srgbClr val="{TINTA}"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="{AZUL}"/></a:dk2><a:lt2><a:srgbClr val="{FONDO}"/></a:lt2>
<a:accent1><a:srgbClr val="{AZUL}"/></a:accent1><a:accent2><a:srgbClr val="{AMARILLO}"/></a:accent2><a:accent3><a:srgbClr val="2E5BBA"/></a:accent3><a:accent4><a:srgbClr val="2B7A78"/></a:accent4><a:accent5><a:srgbClr val="E85D75"/></a:accent5><a:accent6><a:srgbClr val="{GRIS}"/></a:accent6>
<a:hlink><a:srgbClr val="2E5BBA"/></a:hlink><a:folHlink><a:srgbClr val="002F6C"/></a:folHlink></a:clrScheme>
<a:fontScheme name="ITERHUB"><a:majorFont><a:latin typeface="{FUENTE_TIT}"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="{FUENTE_TXT}"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>
<a:fmtScheme name="ITERHUB"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
</a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>"""

GRUPO_VACIO = '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
MAPA = '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'

MAESTRO = CABEZA + f"""<p:sldMaster xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}"><p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg><p:spTree>{GRUPO_VACIO}</p:spTree></p:cSld>
{MAPA}<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
<p:txStyles><p:titleStyle><a:lvl1pPr><a:defRPr sz="3200"><a:latin typeface="+mj-lt"/></a:defRPr></a:lvl1pPr></p:titleStyle><p:bodyStyle><a:lvl1pPr><a:defRPr sz="2000"><a:latin typeface="+mn-lt"/></a:defRPr></a:lvl1pPr></p:bodyStyle><p:otherStyle><a:lvl1pPr><a:defRPr sz="1800"/></a:lvl1pPr></p:otherStyle></p:txStyles></p:sldMaster>"""

DISENO = CABEZA + f"""<p:sldLayout xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}" type="blank" preserve="1"><p:cSld name="En blanco"><p:spTree>{GRUPO_VACIO}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>"""

MAESTRO_NOTAS = CABEZA + f"""<p:notesMaster xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}"><p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg><p:spTree>{GRUPO_VACIO}</p:spTree></p:cSld>{MAPA}</p:notesMaster>"""


def notas_xml(texto, n):
    parrafos = "".join(f'<a:p><a:r><a:rPr lang="es-CO" sz="1200"/><a:t>{e(l)}</a:t></a:r></a:p>' for l in str(texto).split("\n")) or "<a:p/>"
    return CABEZA + f"""<p:notes xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}"><p:cSld><p:spTree>{GRUPO_VACIO}
<p:sp><p:nvSpPr><p:cNvPr id="2" name="Imagen de diapositiva"/><p:cNvSpPr><a:spLocks noGrp="1" noRot="1" noChangeAspect="1"/></p:cNvSpPr><p:nvPr><p:ph type="sldImg"/></p:nvPr></p:nvSpPr><p:spPr/></p:sp>
<p:sp><p:nvSpPr><p:cNvPr id="3" name="Notas"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/>
<p:txBody><a:bodyPr/><a:lstStyle/>{parrafos}</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>"""


def rels(lista):
    filas = "".join(f'<Relationship Id="{i}" Type="{t}" Target="{d}"/>' for i, t, d in lista)
    return CABEZA + f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{filas}</Relationships>'


def crear(datos, salida):
    diapos = datos.get("diapositivas") or []
    if not diapos:
        raise SystemExit("El JSON no tiene 'diapositivas'.")
    usar_formato(datos.get("formato", "16:9"))
    medios = {}
    total = len(diapos)
    construidas = [construir(s, medios, i + 1, total) for i, s in enumerate(diapos)]

    tipos = ['<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
             '<Default Extension="xml" ContentType="application/xml"/>',
             '<Default Extension="png" ContentType="image/png"/>',
             '<Default Extension="jpg" ContentType="image/jpeg"/>',
             '<Default Extension="jpeg" ContentType="image/jpeg"/>',
             '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
             '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
             '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
             '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>',
             '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
             '<Override PartName="/ppt/theme/theme2.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
             '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>',
             '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>',
             '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>',
             '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
             '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>']
    for i in range(1, total + 1):
        tipos.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
        tipos.append(f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>')

    pres_rels = [("rId1", f"{REL}/slideMaster", "slideMasters/slideMaster1.xml"),
                 ("rId2", f"{REL}/notesMaster", "notesMasters/notesMaster1.xml"),
                 ("rId3", f"{REL}/theme", "theme/theme1.xml"),
                 ("rId4", f"{REL}/presProps", "presProps.xml"),
                 ("rId5", f"{REL}/viewProps", "viewProps.xml"),
                 ("rId6", f"{REL}/tableStyles", "tableStyles.xml")]
    ids = ""
    for i in range(1, total + 1):
        pres_rels.append((f"rId{100 + i}", f"{REL}/slide", f"slides/slide{i}.xml"))
        ids += f'<p:sldId id="{255 + i}" r:id="rId{100 + i}"/>'

    presentacion = CABEZA + f"""<p:presentation xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}" saveSubsetFonts="1">
<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst>
<p:sldIdLst>{ids}</p:sldIdLst><p:sldSz cx="{W}" cy="{H}"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle><a:lvl1pPr><a:defRPr lang="es-CO"/></a:lvl1pPr></p:defaultTextStyle></p:presentation>"""

    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    core = CABEZA + f"""<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>{e(datos.get('titulo', 'Presentación ITERHUB'))}</dc:title><dc:creator>{e(datos.get('autor', 'ITERHUB'))}</dc:creator>
<dcterms:created xsi:type="dcterms:W3CDTF">{ahora}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{ahora}</dcterms:modified></cp:coreProperties>"""
    app = CABEZA + f'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>ITERHUB Oficina de Agentes</Application><Slides>{total}</Slides></Properties>'

    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CABEZA + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' + "".join(tipos) + "</Types>")
        z.writestr("_rels/.rels", rels([("rId1", f"{REL}/officeDocument", "ppt/presentation.xml"),
                                        ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
                                        ("rId3", f"{REL}/extended-properties", "docProps/app.xml")]))
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("ppt/presentation.xml", presentacion)
        z.writestr("ppt/_rels/presentation.xml.rels", rels(pres_rels))
        z.writestr("ppt/presProps.xml", CABEZA + f'<p:presentationPr xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}"/>')
        z.writestr("ppt/viewProps.xml", CABEZA + f'<p:viewPr xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}"/>')
        z.writestr("ppt/tableStyles.xml", CABEZA + f'<a:tblStyleLst xmlns:a="{NS_A}" def="{{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}}"/>')
        z.writestr("ppt/theme/theme1.xml", TEMA)
        z.writestr("ppt/theme/theme2.xml", TEMA)
        z.writestr("ppt/slideMasters/slideMaster1.xml", MAESTRO)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels([("rId1", f"{REL}/slideLayout", "../slideLayouts/slideLayout1.xml"), ("rId2", f"{REL}/theme", "../theme/theme1.xml")]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", DISENO)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels([("rId1", f"{REL}/slideMaster", "../slideMasters/slideMaster1.xml")]))
        z.writestr("ppt/notesMasters/notesMaster1.xml", MAESTRO_NOTAS)
        z.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", rels([("rId1", f"{REL}/theme", "../theme/theme2.xml")]))
        for ruta, nombre in medios.items():
            z.write(ruta, f"ppt/media/{nombre}")
        for i, d in enumerate(construidas, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", d.xml())
            r = [("rId1", f"{REL}/slideLayout", "../slideLayouts/slideLayout1.xml"), ("rId2", f"{REL}/notesSlide", f"../notesSlides/notesSlide{i}.xml")]
            r += [(rid, f"{REL}/image", f"../media/{m}") for rid, m in d.imagenes]
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels(r))
            z.writestr(f"ppt/notesSlides/notesSlide{i}.xml", notas_xml(d.notas, i))
            z.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", rels([("rId1", f"{REL}/notesMaster", "../notesMasters/notesMaster1.xml"), ("rId2", f"{REL}/slide", f"../slides/slide{i}.xml")]))
    return total


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(1)
    global CARPETA_JSON
    CARPETA_JSON = Path(sys.argv[1]).resolve().parent
    datos = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    n = crear(datos, sys.argv[2])
    faltan = [i + 1 for i, s in enumerate(datos.get("diapositivas") or []) if (s.get("archivo") or s.get("imagen")) and not buscar_imagen(s.get("archivo") or s.get("imagen"))]
    print(f"Listo: {sys.argv[2]} ({n} diapositivas)" + (f" · imágenes por generar en diapositivas {faltan}: guárdalas en {CARPETA_JSON / 'imagenes'} con el nombre indicado y vuelve a ejecutar este comando." if faltan else ""))


if __name__ == "__main__":
    main()
