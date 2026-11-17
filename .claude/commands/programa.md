---
description: Software para ITERHUB o para un cliente (ej. /programa una landing con formulario de inscripción para el webinar). Página, app, API, automatización o herramienta, con arquitectura, código probado y revisión.
argument-hint: <qué construir, para quién y dónde debe vivir el código>
---
Pedido de software: $ARGUMENTS

Sigue el flujo de CLAUDE.md desde el Paso 0 con tipo de carpeta `pedido` (o `programa`).
- **Paso 0:** pregunta lo que falte: para quién es y quién lo va a usar, qué debe hacer
  exactamente (las 3 a 5 funciones que no pueden faltar), si recoge datos personales y cuáles,
  qué herramientas usa ya la persona (hosting, dominio, CRM, formularios, hojas de cálculo), dónde
  debe quedar el código (`salidas/<tema>/` o una ruta suya), y si hay marca, textos o diseño
  definidos (ITERHUB o el cliente).
- **Entregable principal:** el código funcionando en local en `salidas/<tema>/` (o la ruta
  indicada), con `README.md`, `.env.example` con `[COMPLETAR]` (nunca claves reales),
  `ARQUITECTURA.md` e `informe_pruebas.md` con resultados reales.
- **Equipo:** Snape (arquitectura y tareas en la oleada 1; revisión de código al final); Draco
  si hay interfaz; Bill si hay servidor, API o base de datos; Arthur si hay que conectar
  herramientas o automatizar; Neville (pruebas ejecutadas de verdad) siempre en Profesional y
  Experto; Fred o George solo si hay que escribir los textos de la página; Voldemort en Experto o
  si hay datos personales (ataque a la arquitectura y riesgos de Ley 1581). McGonagall al final.
- **Nada se despliega, se publica ni se conecta a cuentas reales:** todo queda para aprobación.
