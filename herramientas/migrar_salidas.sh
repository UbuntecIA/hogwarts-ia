#!/bin/bash
# Mueve las entregas antiguas (pedidos/<pedido>/entrega/) a salidas/<tema>/ y actualiza las
# referencias en RESUMEN.md, ACTA.md y ORDEN.md. No borra nada: solo mueve y edita textos.
# Uso: bash herramientas/migrar_salidas.sh "<ruta de la carpeta ITERHUB Oficina de Agentes>"
cd "$1" || exit 1
mkdir -p salidas

mover() {  # $1 = carpeta del pedido, $2 = tema
  local pedido="pedidos/$1" tema="$2"
  [ -d "$pedido/entrega" ] || return 0
  mkdir -p "salidas/$tema"
  mv "$pedido/entrega/"* "salidas/$tema/" 2>/dev/null
  for f in "$pedido/RESUMEN.md" "$pedido/ACTA.md"; do
    [ -f "$f" ] && sed -i "s#entrega/#salidas/$tema/#g" "$f"
  done
  if [ -f "$pedido/ORDEN.md" ] && ! grep -q "^Salida:" "$pedido/ORDEN.md"; then
    printf '\nSalida: salidas/%s/\n' "$tema" >> "$pedido/ORDEN.md"
  fi
  if [ -f "$pedido/ACTA.md" ] && ! grep -q "salidas/$tema" "$pedido/ACTA.md"; then
    printf '\nSalida: salidas/%s/\n' "$tema" >> "$pedido/ACTA.md"
  fi
  echo "movido: $pedido/entrega -> salidas/$tema/"
}

mover 2026-11-01_pedido-agentes-pymes post-y-carrusel-agentes-ia-pymes
mover 2026-11-01_contenido-agentes-ia-pymes videos-tiktok-agentes-ia-pymes
mover 2026-11-01_reunion-inscritos-webinar-pymes reunion-inscritos-webinar
