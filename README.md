# Hogwarts IA · oficina de agentes de Claude Code en 3D

Una oficina de **24 agentes de Claude Code** (subagentes) que viven en un castillo 3D de cinco
pisos. Tú hablas con un solo coordinador, **Dumbledore**: él te pregunta lo necesario, propone un
entregable, arma el equipo mínimo (programación, contenido, video, presentaciones, investigación,
cursos o marketing), **se aparece junto a cada agente para darle su misión** y te entrega el
resultado revisado. Mientras no trabajan, los agentes pasean por el castillo. Los tokens que
gasta cada uno se muestran como **puntos de magia**.

> Todo corre en tu computador. El castillo es una página local que habla con **tu propio
> Claude Code**, con **tu propia cuenta**. Este repositorio **no trae ninguna credencial**: cada
> persona pone la suya (ver el paso 3).

Manual de uso (pisos, personajes, reuniones, magia): [LEEME.md](LEEME.md).

---

## 1. Requisitos

| Qué | Para qué | Cómo comprobarlo |
|---|---|---|
| **Claude Code** 2.x | Es el motor: Dumbledore y los agentes son sesiones de Claude Code | `claude --version` |
| **Una cuenta de Claude** (Pro / Max) **o** una clave de la API de Anthropic | Paga los tokens que gastan los agentes | — |
| **Python 3.9+** | El servidor del castillo y los generadores de PPT y Word (solo biblioteca estándar: no hay que instalar nada con pip) | `python3 --version` |
| Un navegador moderno | Ver el castillo 3D (Three.js va incluido en `oficina3d/vendor/`) | — |
| *Opcional:* Node.js y ffmpeg | Para pedidos de programación y de video | `node -v`, `ffmpeg -version` |

Instalar Claude Code: <https://docs.claude.com/en/docs/claude-code/setup>
(en Mac/Linux: `curl -fsSL https://claude.ai/install.sh | bash`).

## 2. Descargarlo

```bash
git clone https://github.com/<TU_USUARIO>/<TU_REPOSITORIO>.git "Hogwarts IA"
cd "Hogwarts IA"
```

## 3. Poner TU credencial de Claude  ⚠️ obligatorio

Los agentes gastan tokens de **la cuenta de quien ejecuta el castillo**. Escoge **una** opción:

**Opción A · Tu suscripción, iniciando sesión (la más simple)**
```bash
claude          # inicia sesión con tu cuenta Pro/Max y sal con /exit
```
No tienes que crear `.env`. El castillo usa esa sesión.

**Opción B · Tu suscripción, con un token de larga duración**
```bash
cp .env.example .env
claude setup-token          # copia el token que te muestra (sk-ant-oat…)
```
Abre `.env` y pégalo en `CLAUDE_CODE_OAUTH_TOKEN=`.

**Opción C · Clave de la API de Anthropic (pago por uso)**
```bash
cp .env.example .env
```
Crea la clave en <https://console.anthropic.com> → *Settings → API Keys* y pégala en
`ANTHROPIC_API_KEY=`. Si esta variable tiene valor, **tiene prioridad** sobre tu suscripción.

> 🔒 `.env` está en `.gitignore` y los agentes tienen prohibido leerlo
> (`configuracion/claude/settings.json` → `deny: Read(./.env)`). **Nunca pegues una clave en
> otro archivo** ni la subas a GitHub. Si la subiste por error, revócala en la consola de Anthropic.

Al encender el servidor verás en la terminal cuál credencial está usando.

## 4. Confiar en la carpeta (una sola vez)

```bash
claude      # dentro de la carpeta del proyecto
```
Acepta *"Do you trust the files in this folder?"* y sal con `/exit`. Sin esto, Claude Code no
carga los agentes ni los hooks que mueven a los personajes.

## 5. Encender el castillo

```bash
python3 oficina3d/servidor.py --abrir
```
(En Windows: `python oficina3d\servidor.py --abrir`.)

Abre <http://localhost:8777>. Deja la terminal abierta; `Ctrl+C` lo apaga.

- **Ver demo**: simula un pedido completo **sin gastar tokens**. Es la mejor forma de probarlo.
- Escríbele a Dumbledore en la barra de abajo, por ejemplo:
  `/programa una landing con formulario para un webinar` o `/presentacion propuesta de IA para un cliente, 20 min`.
- Elige el modelo (Haiku, Sonnet u Opus) en el selector antes de enviar: Opus gasta mucho más.
- *Opcional:* crear un ícono en el escritorio (Mac/Windows): `python3 oficina3d/crear_app.py`.

También puedes trabajar sin el castillo: `claude` en la carpeta y escríbele igual. Si el
castillo está encendido, verás a los agentes moverse igual.

---

## 6. Adaptarlo a tu empresa y a tu Claude

La oficina viene configurada para **ITERHUB** (agencia de marketing y academia de IA en
Colombia). Cambia esto para que trabaje para ti:

### 6.1 Tus datos y tu marca (obligatorio)
El repositorio **no trae datos ni logos de ninguna empresa**: trae plantillas. La primera vez que
enciendes el castillo se crean tus archivos privados (están en `.gitignore`, nunca se suben):

| Archivo (tuyo, privado) | Se crea desde | Qué poner |
|---|---|---|
| `conocimiento/iterhub.md` | `conocimiento/iterhub.ejemplo.md` | Quién eres, qué vendes, a quién, oferta, precios y tono. Lo que no sepas déjalo como `[COMPLETAR: …]`: los agentes nunca lo inventan. |
| `configuracion/marca.md` | `configuracion/marca.ejemplo.md` | Colores, tipografía, tono y reglas de logo. |
| `oficina3d/marca/*.png` | — | Tus logos: `logo_claro.png`, `logo_oscuro.png`, `logo_una_tinta.png` y `logo_castillo.png` (ver `oficina3d/marca/LEEME.md`). Si faltan, nada se rompe. |

Además:
- **Colores de PPT y Word:** la línea `AZUL, AMARILLO, TINTA, …` en `herramientas/crear_pptx.py` (~línea 32) y `herramientas/crear_docx.py` (~línea 23).
- **`CLAUDE.md`:** las instrucciones de Dumbledore. La oficina viene escrita para ITERHUB (agencia de marketing y academia de IA); reemplaza el nombre y ajusta los tipos de pedido que haces:
```bash
grep -rln "ITERHUB" CLAUDE.md conocimiento configuracion herramientas oficina3d
```

### 6.2 Los agentes
- **Fuente de verdad:** `configuracion/claude/` (agents, commands, skills, settings.json).
  Al encender el servidor se copian a `.claude/` (lo anterior queda en `.claude/respaldo-*`).
  **Edita siempre en `configuracion/claude/`**, no en `.claude/`, o se sobrescribe.
- Cada agente es un `.md` con frontmatter (`name`, `description`, `tools`, `model: inherit`).
  El `name` es técnico (p. ej. `investigacion-tematica`) y el personaje (Hermione) va en el texto,
  así puedes cambiar personajes sin romper nada.
- **Agregar un agente:** crea `configuracion/claude/agents/<slug>.md`, agrégalo a la tabla del
  equipo en `CLAUDE.md` y a `oficina3d/equipo.js` (mismo `slug`) para que aparezca en el castillo.
- **Personajes, bios, pisos y apariencia:** `oficina3d/equipo.js`.
- **Modelo por defecto:** `"model": "sonnet"` en `configuracion/claude/settings.json`.

### 6.3 Permisos (qué pueden hacer sin preguntarte)
En `configuracion/claude/settings.json` → `permissions.allow`. Vienen permitidos leer/escribir
en la carpeta, buscar en la web, Python, Node/npm, ffmpeg y git local (**sin** `git push`).
Quita lo que no quieras. Ningún agente publica, envía ni despliega nada.

### 6.4 Conectar herramientas externas (opcional)
`configuracion/mcp.ejemplo.json` es solo un ejemplo: cópialo como `.mcp.json` (ignorado por git)
y pon las URL de **tus** servidores MCP. Ver `configuracion/conectores.md`.

### 6.5 Puerto
Si el 8777 está ocupado, pon otro en `.env` → `HOGWARTS_PUERTO=8790`. Los hooks de Claude Code
se ajustan solos al encender el servidor.

---

## 7. Puntos de magia (tokens)
1 PM ≈ 1.000 tokens ponderados por costo (entrada ×1, caché escrita ×1,25, caché leída ×0,1,
salida ×5). Cada agente tiene una reserva diaria **indicativa** en `oficina3d/equipo.js`
(campo `reserva`): no corta el trabajo, solo pinta la barra en rojo. Se guarda en
`oficina3d/magia.json` (local, no se sube). El consumo real y la facturación los ves en tu
cuenta de Claude o en la consola de Anthropic.

## 8. Estructura
```
CLAUDE.md               instrucciones del coordinador (Dumbledore)
LEEME.md                manual de uso del castillo
.env.example            plantilla de credenciales → copia a .env
configuracion/claude/   agentes, comandos, skills y hooks (se instalan en .claude/)
conocimiento/           lo que el equipo sabe (empresa, métodos, formatos, calidad)
herramientas/           scripts para PPT, Word e integración de entregas
oficina3d/              servidor.py, index.html (castillo 3D), equipo.js (elenco)
pedidos/                trabajo interno de cada pedido (no se sube)
salidas/                entregas finales (no se suben)
```

## 9. Problemas frecuentes
| Síntoma | Solución |
|---|---|
| "No encuentro Claude Code" | Instálalo y verifica `claude --version` en la misma terminal. |
| Los personajes no se mueven con pedidos hechos en la terminal | Falta el paso 4 (confiar en la carpeta) o el castillo está apagado. |
| `Invalid API key` / `401` | Revisa `.env`: una sola credencial, sin comillas ni espacios. Borra la variable para volver a tu sesión. |
| El castillo se ve negro | Ábrelo en Chrome/Edge/Safari actualizados; requiere WebGL. |
| "La oficina ya estaba encendida" | Ya hay un servidor corriendo: abre <http://localhost:8777>. |

## 10. Avisos
- Harry Potter y sus personajes son marcas de Warner Bros. Entertainment. Este es un proyecto
  personal y no comercial sin relación con ellos; los entregables que producen los agentes no
  usan nombres ni referencias a Harry Potter. Si lo usas comercialmente, cambia los personajes.
- Three.js se incluye bajo licencia MIT (`oficina3d/vendor/LICENSE-three.txt`).
- Tú pagas los tokens que gasten los agentes con tu cuenta: empieza con **Ver demo** y con
  pedidos cortos en Haiku o Sonnet.
