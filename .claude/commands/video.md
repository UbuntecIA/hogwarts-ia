---
description: Producción de un video (ej. /video reel de 30 s sobre agentes de IA para pymes). Guion técnico, guion gráfico, prompts para IAs de video, subtítulos y, si entregas grabaciones, la edición con ffmpeg.
argument-hint: <qué video, para qué canal, duración y si hay grabaciones>
---
Video: $ARGUMENTS

Sigue el flujo de CLAUDE.md desde el Paso 0 con tipo de carpeta `pieza` y las skills
`guion-video-corto` y `tendencias-redes`.
- **Paso 0:** pregunta lo que falte: público, canal y formato (9:16, 1:1, 16:9), duración,
  objetivo y llamado a la acción, quién sale en cámara (o si es con voz y texto, o generado con
  IA), si ya hay grabaciones para editar (y su ruta), si hay música con licencia y si es para
  ITERHUB o un cliente.
- **Entregable principal:** el video listo para producir: guion técnico segundo a segundo, guion
  gráfico en tabla, lista de planos, prompts para IAs de video (`prompts_video.md` y `.json`),
  subtítulos `.srt` y texto para publicar; y, si la persona entregó grabaciones, los videos
  editados con `ffmpeg` y verificados con `ffprobe`.
- **Equipo:** Colin (producción y edición); Ginny (tendencias del canal y guion) y Fred
  (ganchos y textos) solo si hace falta escribir el guion desde cero; Luna en Profesional y
  Experto si hay que investigar tendencias o competencia. McGonagall al final.
- **Nada se publica ni se sube a plataformas:** todo queda para aprobación.
