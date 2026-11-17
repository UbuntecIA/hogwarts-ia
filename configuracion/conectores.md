# Cómo se conectarían las herramientas (demo)

En este demo **ninguna herramienta está conectada**: los agentes entregan borradores en
archivos. Esta guía muestra cómo se conectaría cada una cuando quieras pasar a producción.

## Cómo funciona una conexión
Claude Code se conecta a herramientas externas con **servidores MCP**. Cada uno le da a los
agentes acciones nuevas, como "crear borrador de campaña en Meta" o "subir lección a Moodle".

Hay dos formas de agregarlos:
1. **Con el comando**, desde la carpeta del proyecto:
   `claude mcp add --transport http <nombre> <url-del-servidor>`.
2. **Con el archivo `.mcp.json`** en la raíz del proyecto. Hay uno de ejemplo en
   `configuracion/mcp.ejemplo.json`: cópialo como `.mcp.json` y cambia las URL por las reales.

Después, al agente que la usará se le da permiso para esa herramienta en la línea `tools:` de su
archivo en `.claude/agents/`. Por ejemplo, para Ron: `tools: Read, Write, mcp__meta-ads__*`.

## Qué agente usaría cada herramienta

| Herramienta | Agentes | Qué harían conectados |
|---|---|---|
| Meta Ads (Meta Business) | Ron | Crear campañas en borrador y leer resultados reales |
| Meta Business Suite, LinkedIn, TikTok | Ginny | Programar publicaciones en borrador |
| WhatsApp Business | Ginny, Fred | Plantillas y listas de difusión en borrador |
| Canva, Figma, PowerPoint en la nube | Dean, Sprout | Crear diseños a partir de plantillas de marca |
| Google Analytics, Looker Studio, Meta Insights | Luna, Ron | Leer métricas reales para el diagnóstico |
| Notion, Google Drive, Slack | Dumbledore, Lupin | Guardar órdenes y reportes donde trabaja el equipo |
| n8n, Make, Zapier, Google Sheets, CRM | Arthur | Importar flujos y probarlos con datos reales en borrador |
| GitHub, Vercel, Netlify | Snape, Draco, Bill, Neville | Subir el código a un repositorio y desplegar en un entorno de prueba |

## Reglas al conectar
- Empieza con permisos de **solo lectura o borrador**. Ningún agente debe publicar ni gastar
  presupuesto sin que una persona lo apruebe.
- Las claves de acceso van en variables de entorno, nunca escritas en los archivos del proyecto.
