"""Crea el ícono "Hogwarts IA" para abrir la oficina con un clic (Mac o Windows).

Al hacerle clic: enciende el servidor de la oficina (si no está encendido) y abre la oficina 3D
en el navegador.

Uso, una sola vez, desde la carpeta "Hogwarts IA":
    Mac:     python3 oficina3d/crear_app.py
    Windows: python oficina3d\\crear_app.py

- Mac: crea "Hogwarts IA.app" en tu carpeta Aplicaciones personal (~/Applications) y la
  abre para que la arrastres al Dock.
- Windows: crea un acceso directo "Hogwarts IA" con ícono en el Escritorio y en el menú
  Inicio (desde ahí puedes anclarlo a la barra de tareas).

Si mueves la carpeta de lugar, vuelve a ejecutar este script.
"""
import os
import shutil
from datetime import datetime
import stat
import struct
import subprocess
import sys
from pathlib import Path

OFICINA = Path(__file__).resolve().parent
PROYECTO = OFICINA.parent
NOMBRE = "Hogwarts IA"
PUERTO = 8777
TIPOS_ICNS = [("icp4", 16), ("icp5", 32), ("ic07", 128), ("ic08", 256), ("ic09", 512), ("ic10", 1024)]


def comillas_sh(texto):
    return "'" + str(texto).replace("'", "'\\''") + "'"


def comillas_as(texto):
    return '"' + str(texto).replace("\\", "\\\\").replace('"', '\\"') + '"'


# ------------------------------------------------------------------ Mac
def crear_icns(destino):
    bloques = b""
    for tipo, tam in TIPOS_ICNS:
        png = (OFICINA / "icono" / f"icono_{tam}.png").read_bytes()
        bloques += tipo.encode() + struct.pack(">I", len(png) + 8) + png
    destino.write_bytes(b"icns" + struct.pack(">I", len(bloques) + 8) + bloques)


PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>{nombre}</string>
  <key>CFBundleDisplayName</key><string>{nombre}</string>
  <key>CFBundleIdentifier</key><string>co.iterhub.hogwarts-ia</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>oficina</string>
  <key>CFBundleIconFile</key><string>icono</string>
  <key>LSMinimumSystemVersion</key><string>11.0</string>
</dict>
</plist>
"""


def crear_mac():
    destino = Path.home() / "Applications" / f"{NOMBRE}.app"
    if destino.exists():
        shutil.rmtree(destino)
    (destino / "Contents" / "MacOS").mkdir(parents=True)
    (destino / "Contents" / "Resources").mkdir(parents=True)
    (destino / "Contents" / "Info.plist").write_text(PLIST.format(nombre=NOMBRE), encoding="utf-8")
    crear_icns(destino / "Contents" / "Resources" / "icono.icns")
    # El servidor se abre en una ventana de Terminal: Terminal ya tiene permiso para leer Documentos.
    orden = f"cd {comillas_sh(PROYECTO)} && {comillas_sh(sys.executable)} oficina3d/servidor.py --abrir"
    lanzador = f"""#!/bin/bash
# Lanzador de la Hogwarts IA (creado por oficina3d/crear_app.py)
URL="http://localhost:{PUERTO}"
if /usr/bin/curl -s -o /dev/null --max-time 1 "$URL/estado"; then
  /usr/bin/open "$URL"
  exit 0
fi
/usr/bin/osascript -e {comillas_sh('tell application "Terminal" to do script ' + comillas_as(orden))} -e 'tell application "Terminal" to activate'
"""
    ejecutable = destino / "Contents" / "MacOS" / "oficina"
    ejecutable.write_text(lanzador, encoding="utf-8")
    ejecutable.chmod(ejecutable.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    subprocess.run(["touch", str(destino)])
    print(f"Listo: creé {destino}")
    print("Arrástralo al Dock desde la ventana que se abrió. La primera vez macOS te pedirá permiso para")
    print("que la app controle Terminal: elige Permitir.")
    subprocess.run(["open", str(destino.parent)])


# ------------------------------------------------------------------ Windows
def crear_ico(destino):
    tams = [16, 32, 64, 256]
    pngs = [(OFICINA / "icono" / f"icono_{t}.png").read_bytes() for t in tams]
    cab = struct.pack("<HHH", 0, 1, len(tams))
    desplazamiento = 6 + 16 * len(tams)
    entradas, datos = b"", b""
    for t, png in zip(tams, pngs):
        entradas += struct.pack("<BBBBHHII", t % 256, t % 256, 0, 0, 1, 32, len(png), desplazamiento + len(datos))
        datos += png
    destino.write_bytes(cab + entradas + datos)


BAT = r"""@echo off
rem Abre la Hogwarts IA (creado por oficina3d\crear_app.py)
cd /d "%~dp0.."
title Hogwarts IA - deja esta ventana abierta
curl -s -o nul --max-time 1 http://localhost:{puerto}/estado && (start "" http://localhost:{puerto} & exit /b)
where py >nul 2>nul && (py oficina3d\servidor.py --abrir) || (python oficina3d\servidor.py --abrir)
pause
"""


def crear_windows():
    bat = OFICINA / "abrir_oficina.bat"
    bat.write_text(BAT.format(puerto=PUERTO), encoding="ascii")
    ico = OFICINA / "icono" / "icono.ico"
    crear_ico(ico)
    ps = f"""
$s = New-Object -ComObject WScript.Shell
foreach ($carpeta in @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))) {{
  $l = $s.CreateShortcut((Join-Path $carpeta '{NOMBRE}.lnk'))
  $l.TargetPath = '{bat}'
  $l.WorkingDirectory = '{PROYECTO}'
  $l.IconLocation = '{ico}'
  $l.Description = 'Abre la Hogwarts IA'
  $l.Save()
}}
"""
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps], check=True)
    print(f"Listo: creé el acceso directo '{NOMBRE}' en el Escritorio y en el menú Inicio.")
    print("Para anclarlo a la barra de tareas: clic derecho sobre él en el menú Inicio > Anclar a la barra de tareas.")


def instalar_agentes(puerto=None):
    """Instala agentes, comandos, skills y hooks desde configuracion/claude/ en .claude/.

    Las carpetas agents/, commands/ y skills/ se reemplazan completas (lo anterior queda en
    .claude/respaldo-<fecha>/) para que no sobrevivan agentes o comandos que ya no existen.
    settings.json se copia con respaldo .respaldo si cambió.
    """
    # datos de la empresa: si no existen (repositorio recién clonado), se crean desde las plantillas
    for real in (PROYECTO / "conocimiento" / "iterhub.md", PROYECTO / "configuracion" / "marca.md"):
        plantilla = real.with_name(real.stem + ".ejemplo.md")
        if not real.exists() and plantilla.exists():
            shutil.copy2(plantilla, real)
            print(f"Creé {real.relative_to(PROYECTO)} desde la plantilla: llénalo con los datos de tu empresa.")
    origen = PROYECTO / "configuracion" / "claude"
    destino = PROYECTO / ".claude"
    if not origen.exists():
        return
    destino.mkdir(exist_ok=True)
    marca = datetime.now().strftime("%Y-%m-%d_%H%M")
    respaldo = destino / f"respaldo-{marca}"
    cambios = 0
    for carpeta in ("agents", "commands", "skills"):
        nuevo, viejo = origen / carpeta, destino / carpeta
        if not nuevo.exists():
            continue
        if viejo.exists():
            iguales = sorted(p.relative_to(viejo) for p in viejo.rglob("*") if p.is_file()) == sorted(p.relative_to(nuevo) for p in nuevo.rglob("*") if p.is_file()) and all(
                (viejo / p.relative_to(nuevo)).read_bytes() == p.read_bytes() for p in nuevo.rglob("*") if p.is_file())
            if iguales:
                continue
            respaldo.mkdir(exist_ok=True)
            shutil.move(str(viejo), str(respaldo / carpeta))
        shutil.copytree(nuevo, viejo)
        cambios += 1
    ajustes_nuevo, ajustes_viejo = origen / "settings.json", destino / "settings.json"
    if ajustes_nuevo.exists():
        # los hooks avisan al castillo en el puerto configurado (HOGWARTS_PUERTO en .env, 8777 por defecto)
        texto = ajustes_nuevo.read_text(encoding="utf-8")
        if puerto:
            texto = texto.replace("127.0.0.1:8777/", f"127.0.0.1:{puerto}/")
        if not ajustes_viejo.exists() or ajustes_viejo.read_text(encoding="utf-8") != texto:
            if ajustes_viejo.exists():
                shutil.copy2(ajustes_viejo, ajustes_viejo.with_name("settings.json.respaldo"))
            ajustes_viejo.write_text(texto, encoding="utf-8")
            cambios += 1
    if cambios:
        print(f"Agentes, comandos, skills y conexión con la oficina instalados en .claude/ ({cambios} partes actualizadas)."
              + (f" Lo anterior quedó en {respaldo.name}/." if respaldo.exists() else ""))
    else:
        print("Los agentes ya estaban al día.")


def main():
    instalar_agentes()
    if sys.platform == "darwin":
        crear_mac()
    elif os.name == "nt":
        crear_windows()
    else:
        print("Este script crea el ícono en Mac o Windows. En otro sistema, abre la oficina con:")
        print("  python3 oficina3d/servidor.py --abrir")


if __name__ == "__main__":
    main()
