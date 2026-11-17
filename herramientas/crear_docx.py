"""Crea un documento Word (.docx) con la marca ITERHUB a partir de un archivo Markdown.

No necesita instalar nada: usa solo la biblioteca estándar de Python.

Uso:
    python3 herramientas/crear_docx.py documento.md documento.docx [--titulo "…"] [--subtitulo "…"] [--sin-portada]

Soporta: títulos (#, ##, ###), párrafos, viñetas (-, *), listas numeradas (1.), tablas (| a | b |),
citas (>), saltos de página (--- en una línea sola), **negrita**, *cursiva*, `código` y enlaces
[texto](url). Los marcadores [COMPLETAR: …] y [DATO NO ENCONTRADO: …] quedan resaltados en amarillo.
Portada con la marca, encabezado con el título y pie con número de página.
"""
import re
import struct
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
LOGO = RAIZ / "oficina3d" / "marca" / "logo_claro.png"
AZUL, AMARILLO, TINTA, GRIS, FONDO = "002F6C", "FFCC00", "14213D", "5B6578", "F5F7FB"
FUENTE_TIT, FUENTE_TXT = "Poppins", "Inter"
W_NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
CABEZA = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'


def e(t):
    return escape(str(t if t is not None else ""))


# ------------------------------------------------------------------ texto con formato
INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\)|\[(?:COMPLETAR|DATO NO ENCONTRADO)[^\]]*\])")


def runs(texto, base=None):
    """Convierte Markdown en línea a runs de Word."""
    base = dict(base or {})
    partes = []
    for trozo in INLINE.split(texto):
        if not trozo:
            continue
        props = dict(base)
        if trozo.startswith("**") and trozo.endswith("**"):
            props["b"] = True
            trozo = trozo[2:-2]
        elif trozo.startswith("*") and trozo.endswith("*") and len(trozo) > 2:
            props["i"] = True
            trozo = trozo[1:-1]
        elif trozo.startswith("`") and trozo.endswith("`"):
            props["code"] = True
            trozo = trozo[1:-1]
        elif trozo.startswith("[COMPLETAR") or trozo.startswith("[DATO NO ENCONTRADO"):
            props["hl"] = True
            props["b"] = True
        elif trozo.startswith("[") and "](" in trozo:
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", trozo)
            if m:
                trozo = f"{m.group(1)} ({m.group(2)})"
                props["i"] = True
        partes.append(run(trozo, props))
    return "".join(partes)


def run(texto, p):
    rpr = ""
    if p.get("fuente"):
        rpr += f'<w:rFonts w:ascii="{p["fuente"]}" w:hAnsi="{p["fuente"]}" w:cs="{p["fuente"]}"/>'
    if p.get("b"):
        rpr += "<w:b/>"
    if p.get("i"):
        rpr += "<w:i/>"
    if p.get("color"):
        rpr += f'<w:color w:val="{p["color"]}"/>'
    if p.get("tam"):
        rpr += f'<w:sz w:val="{int(p["tam"] * 2)}"/>'
    if p.get("hl"):
        rpr += '<w:highlight w:val="yellow"/>'
    if p.get("code"):
        rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:shd w:val="clear" w:color="auto" w:fill="EEF1F6"/>'
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{e(texto)}</w:t></w:r>'


def parrafo(contenido, estilo=None, ppr_extra="", num=None):
    ppr = ""
    if estilo:
        ppr += f'<w:pStyle w:val="{estilo}"/>'
    if num is not None:
        ppr += f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num}"/></w:numPr>'
    ppr += ppr_extra
    return f"<w:p><w:pPr>{ppr}</w:pPr>{contenido}</w:p>"


def salto_pagina():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def tabla(filas):
    filas = [f for f in filas if f and not all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in f)]
    if not filas:
        return ""
    ncol = max(len(f) for f in filas)
    ancho = int(9000 / ncol)
    xml = ('<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/><w:tblBorders>'
           + "".join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="D5DBE5"/>' for b in ("top", "left", "bottom", "right", "insideH", "insideV"))
           + '</w:tblBorders><w:tblCellMar><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr>'
           + "<w:tblGrid>" + f'<w:gridCol w:w="{ancho}"/>' * ncol + "</w:tblGrid>")
    for i, f in enumerate(filas):
        xml += "<w:tr>"
        for j in range(ncol):
            celda = f[j].strip() if j < len(f) else ""
            fondo = AZUL if i == 0 else (FONDO if i % 2 == 0 else "FFFFFF")
            props = {"b": True, "color": "FFFFFF", "tam": 10} if i == 0 else {"tam": 10}
            xml += (f'<w:tc><w:tcPr><w:tcW w:w="{ancho}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{fondo}"/></w:tcPr>'
                    f'<w:p><w:pPr><w:spacing w:before="60" w:after="60"/></w:pPr>{runs(celda, props)}</w:p></w:tc>')
        xml += "</w:tr>"
    return xml + "</w:tbl><w:p/>"


def imagen_logo(rid, ancho_emu, alto_emu):
    return (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{ancho_emu}" cy="{alto_emu}"/>'
            f'<wp:docPr id="1" name="Logo ITERHUB"/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="logo.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{ancho_emu}" cy="{alto_emu}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')


def tam_png(ruta):
    try:
        with open(ruta, "rb") as f:
            cab = f.read(24)
        if cab[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        return struct.unpack(">II", cab[16:24])
    except OSError:
        return None


# ------------------------------------------------------------------ Markdown → cuerpo
def convertir(md, titulo, subtitulo, con_portada, hay_logo):
    lineas = md.splitlines()
    cuerpo = []
    i = 0
    # título y subtítulo desde el Markdown si no se dieron
    if not titulo:
        for l in lineas:
            if l.startswith("# "):
                titulo = l[2:].strip()
                break
    if con_portada:
        if hay_logo:
            dims = tam_png(LOGO)
            alto = 500000
            ancho = int(alto * dims[0] / dims[1]) if dims else 1800000
            cuerpo.append(parrafo(imagen_logo("rIdLogo", ancho, alto), ppr_extra='<w:spacing w:before="2400" w:after="2400"/>'))
        else:
            cuerpo.append(parrafo(run("ITER", {"b": True, "color": AZUL, "tam": 22, "fuente": FUENTE_TIT}) + run("HUB", {"b": True, "color": AMARILLO, "tam": 22, "fuente": FUENTE_TIT}), ppr_extra='<w:spacing w:before="2400" w:after="2400"/>'))
        cuerpo.append(parrafo(run(titulo or "Documento", {"b": True, "color": AZUL, "tam": 30, "fuente": FUENTE_TIT}), ppr_extra='<w:spacing w:after="400"/>'))
        if subtitulo:
            cuerpo.append(parrafo(run(subtitulo, {"color": GRIS, "tam": 14}), ppr_extra='<w:spacing w:after="200"/>'))
        cuerpo.append(parrafo(run(datetime.now().strftime("%d/%m/%Y"), {"color": GRIS, "tam": 11})))
        cuerpo.append(parrafo(run("Documento de trabajo para aprobación. Los espacios marcados [COMPLETAR] deben llenarse antes de usarlo.", {"color": GRIS, "tam": 9, "i": True}), ppr_extra='<w:spacing w:before="3600"/>'))
        cuerpo.append(salto_pagina())
    primera_h1 = True
    while i < len(lineas):
        l = lineas[i].rstrip()
        if not l.strip():
            i += 1
            continue
        if re.fullmatch(r"\s*-{3,}\s*", l):
            cuerpo.append(salto_pagina())
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", l)
        if m:
            nivel = len(m.group(1))
            texto = m.group(2).strip()
            if nivel == 1 and primera_h1 and con_portada and texto == (titulo or ""):
                primera_h1 = False
                i += 1
                continue  # el título ya está en la portada
            primera_h1 = False
            estilo = {1: "Titulo1", 2: "Titulo2", 3: "Titulo3", 4: "Titulo4"}[nivel]
            cuerpo.append(parrafo(runs(texto), estilo))
            i += 1
            continue
        if l.lstrip().startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].lstrip().startswith("|"):
                fila = lineas[i].strip().strip("|").split("|")
                filas.append([c.strip() for c in fila])
                i += 1
            cuerpo.append(tabla(filas))
            continue
        if l.lstrip().startswith(">"):
            texto = []
            while i < len(lineas) and lineas[i].lstrip().startswith(">"):
                texto.append(lineas[i].lstrip()[1:].strip())
                i += 1
            cuerpo.append(parrafo(runs(" ".join(texto), {"i": True, "color": GRIS}), "Cita"))
            continue
        if l.startswith("```"):
            cod = []
            i += 1
            while i < len(lineas) and not lineas[i].startswith("```"):
                cod.append(lineas[i])
                i += 1
            i += 1
            for c in cod:
                cuerpo.append(parrafo(run(c, {"code": True, "tam": 9}), "Codigo"))
            continue
        m = re.match(r"^\s*[-*•]\s+(.*)$", l)
        if m:
            cuerpo.append(parrafo(runs(m.group(1)), "Lista", num=1))
            i += 1
            continue
        m = re.match(r"^\s*\d+[.)]\s+(.*)$", l)
        if m:
            cuerpo.append(parrafo(runs(m.group(1)), "Lista", num=2))
            i += 1
            continue
        # párrafo: une líneas seguidas
        texto = [l.strip()]
        i += 1
        while i < len(lineas) and lineas[i].strip() and not re.match(r"^(#{1,4}\s|\s*[-*•]\s|\s*\d+[.)]\s|\||>|```|-{3,}\s*$)", lineas[i]):
            texto.append(lineas[i].strip())
            i += 1
        cuerpo.append(parrafo(runs(" ".join(texto)), "Normal"))
    return "".join(cuerpo), titulo


# ------------------------------------------------------------------ partes del paquete
def estilos():
    def st(id_, nombre, tam, color, b=True, fuente=FUENTE_TIT, antes=360, despues=120, base="Normal", extra=""):
        return (f'<w:style w:type="paragraph" w:styleId="{id_}"><w:name w:val="{nombre}"/><w:basedOn w:val="{base}"/><w:qFormat/>'
                f'<w:pPr><w:keepNext/><w:spacing w:before="{antes}" w:after="{despues}"/>{extra}</w:pPr>'
                f'<w:rPr><w:rFonts w:ascii="{fuente}" w:hAnsi="{fuente}"/>{"<w:b/>" if b else ""}<w:color w:val="{color}"/><w:sz w:val="{tam * 2}"/></w:rPr></w:style>')
    return CABEZA + f"""<w:styles {W_NS}>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{FUENTE_TXT}" w:hAnsi="{FUENTE_TXT}" w:cs="{FUENTE_TXT}"/><w:color w:val="{TINTA}"/><w:sz w:val="21"/><w:lang w:val="es-CO"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="140" w:line="300" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
{st("Titulo1", "heading 1", 20, AZUL, antes=480, despues=200, extra=f'<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="{AMARILLO}"/></w:pBdr><w:outlineLvl w:val="0"/>')}
{st("Titulo2", "heading 2", 15, AZUL, antes=360, despues=120, extra='<w:outlineLvl w:val="1"/>')}
{st("Titulo3", "heading 3", 12, TINTA, antes=240, despues=80, extra='<w:outlineLvl w:val="2"/>')}
{st("Titulo4", "heading 4", 11, GRIS, antes=200, despues=60, extra='<w:outlineLvl w:val="3"/>')}
<w:style w:type="paragraph" w:styleId="Lista"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60"/><w:ind w:left="720"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Cita"><w:name w:val="Quote"/><w:basedOn w:val="Normal"/><w:pPr><w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="{AMARILLO}"/></w:pBdr><w:ind w:left="500"/><w:spacing w:before="120" w:after="160"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Codigo"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:shd w:val="clear" w:color="auto" w:fill="EEF1F6"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Encabezado"><w:name w:val="header"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0"/></w:pPr><w:rPr><w:sz w:val="16"/><w:color w:val="{GRIS}"/></w:rPr></w:style>
</w:styles>"""


def numeracion():
    def abstracto(id_, tipo, texto):
        return (f'<w:abstractNum w:abstractNumId="{id_}"><w:multiLevelType w:val="hybridMultilevel"/>'
                f'<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="{tipo}"/><w:lvlText w:val="{texto}"/><w:lvlJc w:val="left"/>'
                f'<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
                + (f'<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:color w:val="{AZUL}"/></w:rPr>' if tipo == "bullet" else "")
                + '</w:lvl></w:abstractNum>')
    return CABEZA + f'<w:numbering {W_NS}>{abstracto(0, "bullet", "■")}{abstracto(1, "decimal", "%1.")}<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num><w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num></w:numbering>'


def encabezado(titulo):
    return CABEZA + f'<w:hdr {W_NS}><w:p><w:pPr><w:pStyle w:val="Encabezado"/><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="{AMARILLO}"/></w:pBdr></w:pPr>{run("ITER", {"b": True, "color": AZUL, "tam": 9, "fuente": FUENTE_TIT})}{run("HUB", {"b": True, "color": AMARILLO, "tam": 9, "fuente": FUENTE_TIT})}{run("   ·   " + (titulo or ""), {"color": GRIS, "tam": 8})}</w:p></w:hdr>'


def pie():
    return CABEZA + f'<w:ftr {W_NS}><w:p><w:pPr><w:pStyle w:val="Encabezado"/><w:jc w:val="right"/></w:pPr>{run("Página ", {"color": GRIS, "tam": 8})}<w:r><w:rPr><w:color w:val="{GRIS}"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:rPr><w:color w:val="{GRIS}"/><w:sz w:val="16"/></w:rPr><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>'


def crear(md, salida, titulo=None, subtitulo=None, con_portada=True):
    hay_logo = bool(tam_png(LOGO))
    cuerpo, titulo = convertir(md, titulo, subtitulo, con_portada, hay_logo)
    documento = CABEZA + f'<w:document {W_NS}><w:body>{cuerpo}<w:sectPr><w:headerReference w:type="default" r:id="rIdHdr"/><w:footerReference w:type="default" r:id="rIdFtr"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1300" w:right="1300" w:bottom="1200" w:left="1300" w:header="600" w:footer="500" w:gutter="0"/></w:sectPr></w:body></w:document>'
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    doc_rels = [("rIdStyles", f"{rel}/styles", "styles.xml"), ("rIdNum", f"{rel}/numbering", "numbering.xml"),
                ("rIdSet", f"{rel}/settings", "settings.xml"), ("rIdHdr", f"{rel}/header", "header1.xml"), ("rIdFtr", f"{rel}/footer", "footer1.xml")]
    if hay_logo:
        doc_rels.append(("rIdLogo", f"{rel}/image", "media/logo.png"))
    rels_xml = lambda lista: CABEZA + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(f'<Relationship Id="{i}" Type="{t}" Target="{d}"/>' for i, t, d in lista) + "</Relationships>"
    tipos = (CABEZA + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/>'
             '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
             '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
             '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
             '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
             '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
             '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
             '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
             '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>')
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    core = (CABEZA + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{e(titulo)}</dc:title><dc:creator>ITERHUB</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">{ahora}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{ahora}</dcterms:modified></cp:coreProperties>')
    app = CABEZA + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>ITERHUB Oficina de Agentes</Application></Properties>'
    settings = CABEZA + f'<w:settings {W_NS}><w:updateFields w:val="true"/><w:defaultTabStop w:val="720"/></w:settings>'
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", tipos)
        z.writestr("_rels/.rels", rels_xml([("rId1", f"{rel}/officeDocument", "word/document.xml"), ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"), ("rId3", f"{rel}/extended-properties", "docProps/app.xml")]))
        z.writestr("word/document.xml", documento)
        z.writestr("word/_rels/document.xml.rels", rels_xml(doc_rels))
        z.writestr("word/styles.xml", estilos())
        z.writestr("word/numbering.xml", numeracion())
        z.writestr("word/settings.xml", settings)
        z.writestr("word/header1.xml", encabezado(titulo))
        z.writestr("word/footer1.xml", pie())
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        if hay_logo:
            z.write(LOGO, "word/media/logo.png")
    return titulo


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    opciones = {}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ("--titulo", "--subtitulo") and i + 1 < len(sys.argv):
            opciones[sys.argv[i][2:]] = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    entrada, salida = Path(args[0]), Path(args[1])
    md = entrada.read_text(encoding="utf-8")
    titulo = crear(md, salida, opciones.get("titulo"), opciones.get("subtitulo"), "--sin-portada" not in sys.argv)
    print(f"Listo: {salida} ({titulo})")


if __name__ == "__main__":
    main()
