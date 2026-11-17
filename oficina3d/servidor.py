"""Servidor local de Hogwarts IA (oficina de agentes de ITERHUB ambientada en Hogwarts).

- Recibe los avisos (hooks) de Claude Code en /evento y los transmite en vivo a la oficina 3D.
- Recibe pedidos desde la oficina (/orden) y los ejecuta con Claude Code en esta carpeta.
- Lista los resultados de la carpeta pedidos/ (/resultados).
- Lleva los puntos de magia (tokens) que gasta cada agente (/magia, guardados en magia.json).

Uso, desde la carpeta "Hogwarts IA":
    Mac:     python3 oficina3d/servidor.py --abrir
    Windows: python oficina3d\\servidor.py --abrir

Solo usa la biblioteca estándar de Python. Escucha únicamente en este computador (127.0.0.1).
"""
import argparse
import json
import re
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

OFICINA = Path(__file__).resolve().parent
PROYECTO = OFICINA.parent
PEDIDOS = PROYECTO / "pedidos"
SALIDAS = PROYECTO / "salidas"


def cargar_env(ruta):
    """Lee el archivo .env de la raíz (CLAVE=valor). No pisa variables ya definidas en el sistema.
    Aquí va la credencial de Claude de cada persona (ver .env.example y README.md)."""
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        clave, valor = clave.strip(), valor.strip().strip('"').strip("'")
        if valor and clave not in os.environ:
            os.environ[clave] = valor


cargar_env(PROYECTO / ".env")
PUERTO = int(os.environ.get("HOGWARTS_PUERTO") or 8777)

EQUIPO = {}
RESERVA = {}
try:
    _txt = (OFICINA / "equipo.js").read_text(encoding="utf-8")
    for a in json.loads(_txt[_txt.index("["):_txt.rindex("]") + 1]):
        EQUIPO[a["slug"]] = a["nombre"]
        RESERVA[a["slug"]] = a.get("reserva", 1500)
except Exception:
    pass

# Versión del servidor: si cambia el código, al abrir la oficina se reemplaza el servidor viejo solo.
VERSION = str(int(Path(__file__).stat().st_mtime))
servidor_http = None

MODELOS = {"haiku", "sonnet", "opus"}
PALABRAS_REUNION = re.compile(r"^\s*/reuni[oó]n\b|lluvia de ideas|brainstorm|sala de juntas|reuni[oó]n de ideas", re.I)
en_reunion = False
# Herramientas que el equipo puede usar sin pedir permiso (igual que .claude/settings.json)
PERMITIDAS = ("Skill Read Write Edit Glob Grep Agent Task WebSearch WebFetch "
              "Bash(mkdir:*) Bash(ls:*) Bash(cp:*) Bash(mv:*) Bash(cat:*) Bash(wc:*) Bash(unzip:*) Bash(python3:*) Bash(python:*) "
              "Bash(node:*) Bash(npm:*) Bash(npx:*) Bash(ffmpeg:*) Bash(ffprobe:*) Bash(which:*) "
              "Bash(git init:*) Bash(git status:*) Bash(git add:*) Bash(git commit:*) Bash(git diff:*) Bash(git log:*)")

# ---------------------------------------------------------------- estado compartido
candado = threading.Lock()
clientes = []          # colas de los navegadores conectados
historial = []         # últimos eventos, para quien se conecte tarde
conversacion = []      # mensajes de Dumbledore y del usuario
proceso = None
sesion_id = None
orden_actual = None


def emitir(ev):
    ev.setdefault("ts", time.time())
    with candado:
        historial.append(ev)
        del historial[:-300]
        for q in list(clientes):
            q.put(ev)


def corto(texto, n=70):
    texto = " ".join(str(texto or "").split())
    return texto if len(texto) <= n else texto[: n - 1] + "…"


def nombre_archivo(ruta):
    return Path(str(ruta or "")).name or "archivo"


def estado_de_herramienta(herr, e):
    if herr in ("Agent", "Task"):
        destino = e.get("subagent_type")
        return "delegando", f"Delegando a {EQUIPO.get(destino, destino)}"
    if herr == "Write":
        return "escribiendo", f"Creando {nombre_archivo(e.get('file_path'))}"
    if herr in ("Edit", "MultiEdit", "NotebookEdit"):
        return "escribiendo", f"Editando {nombre_archivo(e.get('file_path'))}"
    if herr == "Read":
        return "leyendo", f"Leyendo {nombre_archivo(e.get('file_path'))}"
    if herr in ("Glob", "Grep"):
        return "leyendo", "Buscando archivos"
    if herr == "WebSearch":
        return "buscando", f"Buscando: {corto(e.get('query'), 50)}"
    if herr == "WebFetch":
        dominio = urllib.parse.urlparse(str(e.get("url") or "")).netloc
        return "buscando", f"Leyendo {dominio or 'una página'}"
    if herr == "Bash":
        return "ejecutando", corto(e.get("description") or "Ejecutando un comando", 60)
    if str(herr or "").startswith("mcp__"):
        return "ejecutando", f"Usando {herr.split('__')[1]}"
    return "pensando", f"Usando {herr}"


def normalizar(d):
    ev = d.get("hook_event_name") or "Desconocido"
    agente = d.get("agent_type") or "coordinador"
    if agente not in EQUIPO:
        agente = "coordinador" if not d.get("agent_type") else agente
    herr = d.get("tool_name")
    entrada = d.get("tool_input") if isinstance(d.get("tool_input"), dict) else {}
    out = {"tipo": "agente", "evento": ev, "agente": agente, "estado": None, "detalle": "", "destino": None}
    if ev == "SessionStart":
        out.update(agente="coordinador", estado="pensando", detalle="Llegó a Hogwarts")
    elif ev == "UserPromptSubmit":
        prompt = str(d.get("prompt") or "")
        if prompt.lstrip().startswith("<task-notification"):
            out.update(agente="coordinador", estado="revisando", detalle="Recibió la entrega de un agente")
        else:
            out.update(agente="coordinador", estado="pensando", detalle=f"Pedido: {corto(prompt, 70)}")
    elif ev == "PreToolUse":
        estado, detalle = estado_de_herramienta(herr, entrada)
        out.update(estado=estado, detalle=detalle)
        if herr in ("Agent", "Task"):
            out["destino"] = entrada.get("subagent_type")
            out["tarea"] = corto(entrada.get("description") or str(entrada.get("prompt") or "").split("\n")[0], 90)
    elif ev == "PostToolUse":
        if herr in ("Agent", "Task"):
            destino = entrada.get("subagent_type")
            out.update(estado="revisando", detalle=f"Revisando la entrega de {EQUIPO.get(destino, destino)}", destino=destino)
        else:
            out.update(estado="pensando", detalle="Analizando el resultado")
    elif ev == "SubagentStart":
        out.update(estado="llegando", detalle="Empieza su turno")
    elif ev == "SubagentStop":
        out.update(estado="terminado", detalle=corto(d.get("last_assistant_message") or "Entregó su trabajo", 90))
    elif ev == "Notification":
        out.update(estado="esperando", detalle=corto(d.get("message") or "Necesita tu atención", 80))
    elif ev == "Stop":
        out.update(agente="coordinador", estado="terminado", detalle="Pedido terminado")
    else:
        out.update(estado="pensando", detalle=ev)
    return out


# ---------------------------------------------------------------- plan de trabajo por oleadas
POR_NOMBRE = {n.lower(): slug for slug, n in EQUIPO.items()}
LINEA_PLAN = re.compile(r"^\s*[-*]?\s*\**\s*(Oleada\s*(\d+)|Revisi[oó]n|Cierre)\**\s*(?:[·(\-–—]\s*(en paralelo|en cascada|paralelo|cascada)\s*\)?)?\s*\**\s*:\s*\**\s*(.+)$", re.I)


def partir(texto):
    """Separa 'A (x, y) | B (z)' o 'A (x), B (z)' respetando los paréntesis."""
    if "|" in texto:
        return [t.strip() for t in texto.split("|") if t.strip()]
    partes, prof, actual = [], 0, ""
    for ch in texto:
        prof += (ch == "(") - (ch == ")")
        if ch in ",;" and prof == 0:
            partes.append(actual.strip())
            actual = ""
        else:
            actual += ch
    return [t for t in partes + [actual.strip()] if t]


def leer_plan(orden):
    try:
        txt = orden.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    oleadas = []
    for linea in txt.splitlines():
        m = LINEA_PLAN.match(linea)
        if not m:
            continue
        etiqueta = m.group(1)
        tipo = "oleada" if m.group(2) else ("revision" if etiqueta.lower().startswith("revis") else "cierre")
        modo = "cascada" if (m.group(3) or "").lower().endswith("cascada") else "paralelo"
        agentes = []
        for item in partir(m.group(4)):
            mm = re.match(r"^\**([\wÁÉÍÓÚáéíóúñÑ\-]+)\**\s*(?:\((.*)\))?", item)
            if not mm:
                continue
            clave = mm.group(1)
            slug = POR_NOMBRE.get(clave.lower()) or (clave if clave in EQUIPO else None)
            if slug and slug not in [a["slug"] for a in agentes]:
                tarea = mm.group(2) or ""
                mins = re.search(r"~?\s*(\d+(?:[.,]\d+)?)\s*(?:-|–|a)?\s*(\d+(?:[.,]\d+)?)?\s*min", tarea)
                minutos = None
                if mins:
                    a_, b_ = float(mins.group(1).replace(",", ".")), mins.group(2)
                    minutos = (a_ + float(b_.replace(",", "."))) / 2 if b_ else a_
                    tarea = (tarea[:mins.start()] + tarea[mins.end():]).strip(" ·;,-–")
                agentes.append({"slug": slug, "nombre": EQUIPO[slug], "tarea": corto(tarea, 80), "min": minutos})
        if agentes:
            oleadas.append({"tipo": tipo, "n": int(m.group(2)) if m.group(2) else None, "modo": modo, "agentes": agentes})
    if not oleadas:
        return None
    mn = re.search(r"NIVEL\**\s*[:=·-]?\s*\**\s*(B[aá]sico|Profesional|Experto)", txt, re.I)
    nivel = normal_nivel(mn.group(1)) if mn else None
    return {"carpeta": orden.parent.name, "oleadas": oleadas, "ts": orden.stat().st_mtime, "nivel": nivel}


def plan_reciente(horas=6):
    if not PEDIDOS.exists():
        return None
    ordenes = sorted(PEDIDOS.glob("*/ORDEN.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    for o in ordenes[:3]:
        if time.time() - o.stat().st_mtime > horas * 3600:
            break
        plan = leer_plan(o)
        if plan:
            return plan
    return None


def revisar_plan(d):
    """Si alguien escribió o editó un ORDEN.md, avisa a la oficina el plan de oleadas."""
    entrada = d.get("tool_input") if isinstance(d.get("tool_input"), dict) else {}
    ruta = str(entrada.get("file_path") or "")
    if d.get("hook_event_name") == "PostToolUse" and d.get("tool_name") in ("Write", "Edit", "MultiEdit") and ruta.endswith("ORDEN.md"):
        p = Path(ruta)
        if not p.is_absolute():
            p = PROYECTO / p
        plan = leer_plan(p)
        if plan:
            global nivel_actual
            if plan.get("nivel"):
                nivel_actual = plan["nivel"]
            emitir({"tipo": "plan", "modelo": modelo_actual, **plan})


# ---------------------------------------------------------------- tiempos reales de cada agente (la oficina aprende)
TIEMPOS = OFICINA / "tiempos.json"
inicio_agente = {}
nivel_actual = None
modelo_actual = None
candado_tiempos = threading.Lock()


def normal_nivel(t):
    t = (t or "").lower().replace("á", "a")
    return t if t in ("basico", "profesional", "experto") else None


def leer_tiempos():
    try:
        return json.loads(TIEMPOS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []


def guardar_tiempo(agente, segundos):
    if segundos < 5:
        return
    with candado_tiempos:
        datos = leer_tiempos()
        datos.append({"agente": agente, "nivel": nivel_actual or "profesional", "modelo": modelo_actual or "sonnet",
                      "seg": round(segundos), "fecha": time.strftime("%Y-%m-%d %H:%M")})
        tmp = TIEMPOS.with_suffix(".tmp")
        tmp.write_text(json.dumps(datos[-400:], ensure_ascii=False, indent=0), encoding="utf-8")
        tmp.replace(TIEMPOS)


def registrar_tiempos(d):
    ev, herr = d.get("hook_event_name"), d.get("tool_name")
    entrada = d.get("tool_input") if isinstance(d.get("tool_input"), dict) else {}
    agente, ahora = d.get("agent_type"), time.time()
    if ev == "SubagentStart" and agente in EQUIPO:
        inicio_agente.setdefault(agente, ahora)
    elif ev == "PreToolUse" and herr in ("Agent", "Task") and entrada.get("subagent_type") in EQUIPO:
        inicio_agente.setdefault(entrada["subagent_type"], ahora)
    elif ev == "SubagentStop" and agente in inicio_agente:
        guardar_tiempo(agente, ahora - inicio_agente.pop(agente))
    elif ev == "PostToolUse" and herr in ("Agent", "Task") and not entrada.get("run_in_background"):
        destino = entrada.get("subagent_type")
        if destino in inicio_agente:
            guardar_tiempo(destino, ahora - inicio_agente.pop(destino))


def resumen_tiempos():
    """Mediana de segundos por agente|nivel|modelo y por agente|nivel."""
    grupos = {}
    for r in leer_tiempos()[-400:]:
        for k in (f"{r['agente']}|{r['nivel']}|{r['modelo']}", f"{r['agente']}|{r['nivel']}"):
            grupos.setdefault(k, []).append(r["seg"])
    salida = {}
    for k, v in grupos.items():
        v = sorted(v)
        salida[k] = {"med": v[len(v) // 2], "n": len(v)}
    return salida



# ---------------------------------------------------------------- puntos de magia (tokens)
# 1 PM ≈ 1.000 tokens ponderados por su costo real: entrada ×1, escritura de caché ×1,25, lectura de caché ×0,1, salida ×5.
MAGIA = OFICINA / "magia.json"
candado_magia = threading.Lock()
vistos_msg = set()              # id de mensajes ya contados (el stream y las transcripciones se cruzan)
uso_por_tool = {}               # tool_use_id de una llamada a Agent → slug del agente


def pm_de(u):
    return (u.get("input_tokens", 0) + 1.25 * u.get("cache_creation_input_tokens", 0)
            + 0.1 * u.get("cache_read_input_tokens", 0) + 5 * u.get("output_tokens", 0)) / 1000


def leer_magia():
    try:
        d = json.loads(MAGIA.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        d = {}
    d.setdefault("dia", time.strftime("%Y-%m-%d"))
    d.setdefault("hoy", {})
    d.setdefault("total", {})
    d.setdefault("leidos", {})
    if d["dia"] != time.strftime("%Y-%m-%d"):      # cada día la reserva se recarga
        d["dia"], d["hoy"] = time.strftime("%Y-%m-%d"), {}
    return d


def guardar_magia(d):
    d["leidos"] = dict(list(d["leidos"].items())[-300:])
    tmp = MAGIA.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(MAGIA)


def gastar(slug, uso, msg_id=None, tarea=False):
    """Suma el gasto de un mensaje (o una tarea nueva) al agente y lo avisa al castillo."""
    if slug not in EQUIPO:
        slug = "coordinador"
    with candado_magia:
        if msg_id:
            if msg_id in vistos_msg:
                return
            vistos_msg.add(msg_id)
            if len(vistos_msg) > 20000:
                vistos_msg.clear()
        d = leer_magia()
        t = d["total"].setdefault(slug, {"pm": 0, "entrada": 0, "salida": 0, "cache_leida": 0, "cache_escrita": 0, "tareas": 0})
        pm = pm_de(uso or {})
        t["pm"] = round(t["pm"] + pm, 3)
        t["entrada"] += (uso or {}).get("input_tokens", 0)
        t["salida"] += (uso or {}).get("output_tokens", 0)
        t["cache_leida"] += (uso or {}).get("cache_read_input_tokens", 0)
        t["cache_escrita"] += (uso or {}).get("cache_creation_input_tokens", 0)
        if tarea:
            t["tareas"] += 1
        d["hoy"][slug] = round(d["hoy"].get(slug, 0) + pm, 3)
        guardar_magia(d)
        hoy = d["hoy"][slug]
    if pm or tarea:
        emitir({"tipo": "magia", "agente": slug, "gasto": round(pm, 2), "hoy": round(hoy, 2),
                "reserva": RESERVA.get(slug, 1500), "total": round(t["pm"], 2), "tareas": t["tareas"]})


def magia_del_stream(m):
    """Mensajes de stream-json de la corrida lanzada desde el castillo."""
    if m.get("type") != "assistant":
        return
    msg = m.get("message") or {}
    for b in msg.get("content") or []:
        if b.get("type") == "tool_use" and b.get("name") in ("Agent", "Task"):
            uso_por_tool[b.get("id")] = (b.get("input") or {}).get("subagent_type")
    padre = m.get("parent_tool_use_id")
    slug = uso_por_tool.get(padre, "coordinador") if padre else "coordinador"
    if msg.get("usage") and msg.get("id"):
        gastar(slug, msg["usage"], msg["id"])


def magia_de_transcripcion(ruta, slug, solo_principal=False):
    """Lee una transcripción .jsonl desde donde quedó y suma lo que falte (sirve también si usas Claude Code en la terminal)."""
    p = Path(str(ruta or "")).expanduser()
    if not p.is_file():
        return
    with candado_magia:
        desde = leer_magia()["leidos"].get(str(p), 0)
    tam = p.stat().st_size
    if tam <= desde:
        return
    with p.open("rb") as f:
        f.seek(desde)
        datos = f.read()
    corte = datos.rfind(b"\n") + 1
    for linea in datos[:corte].splitlines():
        try:
            r = json.loads(linea)
        except ValueError:
            continue
        if r.get("type") != "assistant" or (solo_principal and r.get("isSidechain")):
            continue
        msg = r.get("message") or {}
        if msg.get("usage") and msg.get("id"):
            gastar(slug, msg["usage"], msg["id"])
    with candado_magia:
        d = leer_magia()
        d["leidos"][str(p)] = desde + corte
        guardar_magia(d)


def magia_de_hook(d):
    ev = d.get("hook_event_name")
    entrada = d.get("tool_input") if isinstance(d.get("tool_input"), dict) else {}
    if ev == "PreToolUse" and d.get("tool_name") in ("Agent", "Task") and entrada.get("subagent_type") in EQUIPO:
        gastar(entrada["subagent_type"], {}, tarea=True)
    elif ev == "SubagentStop":
        slug = d.get("agent_type") if d.get("agent_type") in EQUIPO else "coordinador"
        magia_de_transcripcion(d.get("agent_transcript_path"), slug)
    elif ev in ("Stop", "PostToolUse") and not d.get("agent_type"):
        if ev == "Stop" or d.get("tool_name") in ("Agent", "Task"):
            magia_de_transcripcion(d.get("transcript_path"), "coordinador", solo_principal=True)


def estado_magia():
    d = leer_magia()
    return {"dia": d["dia"], "hoy": d["hoy"], "total": d["total"], "reserva": RESERVA,
            "regla": "1 PM ≈ 1.000 tokens ponderados por costo: entrada ×1, caché escrita ×1,25, caché leída ×0,1, salida ×5"}


# ---------------------------------------------------------------- pedidos con Claude Code
def ejecutable_claude():
    ruta = shutil.which("claude")
    if ruta:
        return ruta
    for c in (Path.home() / ".local/bin/claude", Path("/opt/homebrew/bin/claude"), Path("/usr/local/bin/claude"),
              Path.home() / ".claude/local/claude", Path(os.environ.get("APPDATA", "")) / "npm/claude.cmd",
              Path.home() / ".local/bin/claude.exe",   # instalador oficial en Windows
              Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/WinGet/Links/claude.exe"):
        if c.exists():
            return str(c)
    return None


def correr_orden(texto, modelo, nueva):
    global proceso, sesion_id, orden_actual, en_reunion, nivel_actual, modelo_actual
    claude = ejecutable_claude()
    if not claude:
        emitir({"tipo": "respuesta", "error": True,
                "texto": "No encuentro Claude Code en este computador. Instálalo y abre `claude` una vez para iniciar sesión (ver LEEME.md)."})
        return
    if nueva:
        sesion_id = None
        en_reunion = False
    if PALABRAS_REUNION.search(texto):
        en_reunion = True
    if nueva:
        nivel_actual = None
    m_nivel = re.search(r"Nivel:\s*(B[aá]sico|Profesional|Experto)", texto, re.I)
    if m_nivel:
        nivel_actual = normal_nivel(m_nivel.group(1))
    modelo_actual = modelo
    inicio_agente.clear()
    texto_claude = f"{texto}\n\n[Modelo seleccionado en la oficina: {modelo}]"
    cmd = [claude, "-p", texto_claude, "--output-format", "stream-json", "--verbose",
           "--model", modelo, "--permission-mode", "acceptEdits",
           "--allowedTools", PERMITIDAS]
    if sesion_id:
        cmd += ["--resume", sesion_id]
    entorno = dict(os.environ)
    entorno.pop("CLAUDE_CODE_SUBAGENT_MODEL", None)   # los agentes heredan el modelo de la sesión (model: inherit)
    inicio = time.time()
    orden_actual = {"texto": texto, "modelo": modelo, "inicio": inicio}
    conversacion.append({"quien": "Tú", "texto": texto, "ts": inicio})
    emitir({"tipo": "orden", "estado": "trabajando", "texto": texto, "modelo": modelo, "reunion": en_reunion, "nivel": nivel_actual})
    try:
        proceso = subprocess.Popen(cmd, cwd=PROYECTO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.DEVNULL, env=entorno, text=True, encoding="utf-8",
                                   errors="replace", bufsize=1)
    except OSError as e:
        emitir({"tipo": "respuesta", "error": True, "texto": f"No pude iniciar Claude Code: {e}"})
        orden_actual = None
        return
    final = None
    for linea in proceso.stdout:
        try:
            m = json.loads(linea)
        except ValueError:
            continue
        if m.get("session_id"):
            sesion_id = m["session_id"]
        try:
            magia_del_stream(m)
        except Exception:
            pass
        if m.get("type") == "assistant" and not m.get("parent_tool_use_id"):
            for b in (m.get("message") or {}).get("content") or []:
                if b.get("type") == "text" and b.get("text", "").strip():
                    emitir({"tipo": "dice", "agente": "coordinador", "texto": b["text"].strip()})
        elif m.get("type") == "result":
            final = m
    proceso.wait()
    error_txt = proceso.stderr.read().strip() if proceso.stderr else ""
    detenido = proceso.returncode not in (0, None) and final is None and orden_actual is None
    texto_final = (final or {}).get("result") or (error_txt[-400:] if error_txt else "La corrida terminó sin respuesta.")
    if detenido:
        texto_final = "Pedido detenido."
    respuesta = {"tipo": "respuesta", "texto": texto_final,
                 "error": bool(final and final.get("is_error")) or (final is None and not detenido),
                 "briefing": texto_final.lstrip("`*# \n").upper().startswith("BRIEFING"),
                 "preguntas": texto_final.lstrip("`*# \n").upper().startswith("PREGUNTAS"),
                 "reunion": en_reunion, "acta": en_reunion and "acta" in texto_final[:300].lower(),
                 "duracion": round(time.time() - inicio), "costo": (final or {}).get("total_cost_usd"),
                 "salida": salida_reciente(inicio)}
    conversacion.append({"quien": "Dumbledore", "texto": texto_final, "ts": time.time()})
    emitir(respuesta)
    emitir({"tipo": "agente", "evento": "Stop", "agente": "coordinador", "estado": "terminado",
            "detalle": "Tiene preguntas para ti" if respuesta["preguntas"] else "Esperando tu respuesta" if respuesta["briefing"] else "Pedido terminado"})
    if respuesta["acta"]:
        en_reunion = False
    proceso = None
    orden_actual = None


# ---------------------------------------------------------------- resultados
def archivos_de(carpeta):
    """Archivos de una carpeta, con ruta relativa al proyecto (pedidos/… o salidas/…)."""
    return sorted(str(f.relative_to(PROYECTO)).replace("\\", "/") for f in carpeta.rglob("*")
                  if f.is_file() and not f.name.startswith("."))


def salida_de_pedido(c):
    """Carpeta de salidas que el pedido anotó en ORDEN.md o RESUMEN.md (Salida: salidas/<tema>/)."""
    for n in ("ORDEN.md", "RESUMEN.md", "ACTA.md"):
        f = c / n
        if f.exists():
            m = re.search(r"salidas/([\w.\-]+)", f.read_text(encoding="utf-8", errors="replace"))
            if m and (SALIDAS / m.group(1)).is_dir():
                return m.group(1)
    return None


def listar_resultados():
    if not PEDIDOS.exists():
        return []
    salida = []
    for c in sorted((p for p in PEDIDOS.iterdir() if p.is_dir()), key=lambda p: p.name, reverse=True)[:50]:
        archivos = archivos_de(c)
        resumen = next((c / n for n in ("RESUMEN.md", "REPORTE.md") if (c / n).exists()), None)
        tema = salida_de_pedido(c)
        entrega = archivos_de(SALIDAS / tema) if tema else [a for a in archivos if "/entrega/" in a]
        salida.append({"carpeta": c.name, "archivos": archivos, "entrega": entrega, "salida": tema,
                       "resumen_archivo": str(resumen.relative_to(PROYECTO)).replace("\\", "/") if resumen else "",
                       "reporte": resumen.read_text(encoding="utf-8", errors="replace")[:4000] if resumen else ""})
    return salida


def listar_salidas():
    if not SALIDAS.exists():
        return []
    temas = []
    for c in (p for p in SALIDAS.iterdir() if p.is_dir()):
        archivos = archivos_de(c)
        if not archivos:
            continue
        ultimo = max((PROYECTO / a).stat().st_mtime for a in archivos)
        temas.append({"tema": c.name, "archivos": archivos, "modificado": ultimo})
    return sorted(temas, key=lambda t: -t["modificado"])


def salida_reciente(desde):
    """La carpeta de salidas que se tocó durante la última corrida."""
    recientes = [t for t in listar_salidas() if t["modificado"] >= desde - 5]
    return recientes[0]["tema"] if recientes else None


def ruta_segura(rel):
    p = (PROYECTO / rel).resolve()
    for base in (PEDIDOS.resolve(), SALIDAS.resolve()):
        if base in p.parents or p == base:
            return p
    return None


TIPOS = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".json": "application/json; charset=utf-8", ".md": "text/plain; charset=utf-8", ".txt": "text/plain; charset=utf-8",
         ".csv": "text/plain; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".svg": "image/svg+xml", ".webp": "image/webp", ".ico": "image/x-icon", ".gift": "text/plain; charset=utf-8",
         ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
         ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".pdf": "application/pdf"}
DESCARGAR = {".pptx", ".docx", ".gift", ".json", ".csv"}


class Manejador(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def responder(self, codigo, cuerpo, tipo="application/json; charset=utf-8", descarga=None):
        if isinstance(cuerpo, (dict, list)):
            cuerpo = json.dumps(cuerpo, ensure_ascii=False)
        if isinstance(cuerpo, str):
            cuerpo = cuerpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        if descarga:
            self.send_header("Content-Disposition", "attachment; filename*=UTF-8''" + urllib.parse.quote(descarga))
        self.end_headers()
        self.wfile.write(cuerpo)

    def leer_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return {}

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(url.query)
        if url.path == "/estado":
            return self.responder(200, {"ok": True, "version": VERSION, "trabajando": orden_actual is not None,
                                        "sesion": bool(sesion_id), "claude": bool(ejecutable_claude())})
        if url.path == "/eventos":
            return self.sse()
        if url.path == "/resultados":
            return self.responder(200, listar_resultados())
        if url.path == "/magia":
            return self.responder(200, estado_magia())
        if url.path == "/tiempos":
            return self.responder(200, resumen_tiempos())
        if url.path == "/plan":
            return self.responder(200, plan_reciente() or {})
        if url.path == "/salidas":
            return self.responder(200, listar_salidas())
        if url.path == "/conversacion":
            return self.responder(200, conversacion[-40:])
        if url.path == "/archivo":
            p = ruta_segura(q.get("ruta", [""])[0])
            if not p or not p.is_file():
                return self.responder(404, {"error": "no existe"})
            bajar = q.get("descargar", ["0"])[0] == "1" or p.suffix.lower() in (".pptx", ".docx")
            return self.responder(200, p.read_bytes(), TIPOS.get(p.suffix.lower(), "application/octet-stream"),
                                  descarga=p.name if bajar else None)
        if url.path.startswith("/ver/"):   # páginas de salidas con sus rutas relativas (logos, imágenes)
            rel = urllib.parse.unquote(url.path[len("/ver/"):])
            p = ruta_segura(rel)
            if p is None and rel.startswith("oficina3d/"):
                p = (PROYECTO / rel).resolve()
                if OFICINA not in p.parents:
                    p = None
            if not p or not p.is_file():
                return self.responder(404, {"error": "no existe"})
            return self.responder(200, p.read_bytes(), TIPOS.get(p.suffix.lower(), "application/octet-stream"))
        if url.path == "/abrir-carpeta":
            p = ruta_segura(q.get("ruta", ["pedidos"])[0]) or PEDIDOS
            PEDIDOS.mkdir(exist_ok=True)
            SALIDAS.mkdir(exist_ok=True)
            if sys.platform == "darwin":
                subprocess.Popen(["open", str(p)])
            elif os.name == "nt":
                os.startfile(str(p))  # noqa
            else:
                subprocess.Popen(["xdg-open", str(p)])
            return self.responder(200, {"ok": True})
        # archivos de la oficina
        rel = "index.html" if url.path in ("/", "") else urllib.parse.unquote(url.path.lstrip("/"))
        p = (OFICINA / rel).resolve()
        if OFICINA not in p.parents or not p.is_file():
            return self.responder(404, {"error": "no existe"})
        return self.responder(200, p.read_bytes(), TIPOS.get(p.suffix.lower(), "application/octet-stream"))

    def do_POST(self):
        global proceso, orden_actual
        url = urllib.parse.urlparse(self.path)
        datos = self.leer_json()
        if url.path == "/evento":
            emitir(normalizar(datos))
            for funcion in (revisar_plan, registrar_tiempos, magia_de_hook):
                try:
                    funcion(datos)
                except Exception:
                    pass
            return self.responder(200, {})
        if url.path == "/orden":
            texto = str(datos.get("texto") or "").strip()
            modelo = datos.get("modelo") if datos.get("modelo") in MODELOS else "sonnet"
            if not texto:
                return self.responder(400, {"error": "Escribe un pedido."})
            if orden_actual is not None:
                return self.responder(409, {"error": "La oficina ya está trabajando en un pedido."})
            threading.Thread(target=correr_orden, args=(texto, modelo, bool(datos.get("nueva"))), daemon=True).start()
            return self.responder(200, {"ok": True})
        if url.path == "/detener":
            p = proceso
            orden_actual = None
            if p and p.poll() is None:
                p.terminate()
            return self.responder(200, {"ok": True})
        if url.path == "/apagar":   # lo usa una versión nueva del servidor para reemplazar a esta
            if orden_actual is not None:
                return self.responder(409, {"error": "trabajando"})
            self.responder(200, {"ok": True})
            threading.Thread(target=servidor_http.shutdown, daemon=True).start()
            return
        if url.path == "/nueva":
            globals()["sesion_id"] = None
            conversacion.clear()
            return self.responder(200, {"ok": True})
        return self.responder(404, {"error": "no existe"})

    def sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        q = queue.Queue()
        with candado:
            previos = list(historial[-60:])
            clientes.append(q)
        try:
            for ev in previos:
                self.wfile.write(f"data: {json.dumps(dict(ev, repeticion=True), ensure_ascii=False)}\n\n".encode())
            self.wfile.flush()
            while True:
                try:
                    ev = q.get(timeout=15)
                    self.wfile.write(f"data: {json.dumps(ev, ensure_ascii=False)}\n\n".encode())
                except queue.Empty:
                    self.wfile.write(b": latido\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            with candado:
                if q in clientes:
                    clientes.remove(q)


def ya_encendido(puerto):
    """None si no hay servidor; si lo hay, su /estado."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{puerto}/estado", timeout=1) as r:
            return json.loads(r.read().decode("utf-8")) if r.status == 200 else None
    except Exception:
        return None


def apagar_viejo(puerto):
    """Pide al servidor viejo que se apague (las versiones antiguas no saben: hay que cerrar su ventana)."""
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{puerto}/apagar", data=b"{}", method="POST",
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=2).read()
    except Exception:
        return False
    for _ in range(20):
        time.sleep(0.25)
        if ya_encendido(puerto) is None:
            return True
    return False


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--puerto", type=int, default=PUERTO)
    p.add_argument("--abrir", action="store_true", help="Abrir la oficina en el navegador")
    a = p.parse_args()
    url = f"http://localhost:{a.puerto}"
    global servidor_http
    previo = ya_encendido(a.puerto)
    if previo is not None:
        if previo.get("version") == VERSION or previo.get("trabajando") or not apagar_viejo(a.puerto):
            if previo.get("version") != VERSION:
                print("Hay una versión anterior de la oficina encendida. Para usar la nueva, cierra su ventana de Terminal y vuelve a abrir el ícono.")
            print("La oficina ya estaba encendida:", url)
            if a.abrir:
                webbrowser.open(url)
            return
        print("Reemplacé el servidor anterior por la versión nueva.")
    PEDIDOS.mkdir(exist_ok=True)
    SALIDAS.mkdir(exist_ok=True)
    try:   # instala (o actualiza) los agentes, comandos y skills desde configuracion/claude/
        sys.path.insert(0, str(OFICINA))
        from crear_app import instalar_agentes
        instalar_agentes(a.puerto)
    except Exception as err:
        print("Aviso: no pude actualizar los agentes en .claude/:", err)
    servidor = servidor_http = ThreadingHTTPServer(("127.0.0.1", a.puerto), Manejador)
    servidor.daemon_threads = True
    print(f"Hogwarts IA encendido en {url}")
    print("Deja esta ventana abierta. Para apagar el castillo, ciérrala o presiona Ctrl+C.")
    if not ejecutable_claude():
        print("Aviso: no encuentro Claude Code. La oficina abre, pero no podrá ejecutar pedidos.")
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("Credencial: ANTHROPIC_API_KEY del archivo .env (se cobra a esa cuenta de la API de Anthropic).")
    elif os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
        print("Credencial: CLAUDE_CODE_OAUTH_TOKEN del archivo .env (tu suscripción Pro/Max).")
    else:
        print("Credencial: la sesión con la que iniciaste `claude` en este computador (sin .env).")
    if a.abrir:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nOficina apagada.")


if __name__ == "__main__":
    main()
