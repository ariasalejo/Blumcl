# 🎛️ Módulo: Terminal de Mando (app.py)

## Propósito
Puerta de entrada única de Blumcl. Menú por números validado.

## Mapa de módulos

```text
               ┌────────────────┐
               │ app.py  v0.3.0 │
               └───────┬────────┘
  ┌──────┬──────┬──────┼─────────────┐
  ▼      ▼      ▼      ▼      ▼       ▼
[1]    [2]    [5]    [6]    [8/9]   [7]
scan   html   ia     diag   config  clean
  │      │      │      │      │       │
  ▼      ▼      ▼      ▼      ▼       ▼
scanners reports ai     scanner utils  cleaner
storage  html.py local  .py    config  (M4)
         (M2)   .py            .py
[3/4] → analysis/comparar.py (M3)

## Reglas
- Opción inválida → aviso amable, nunca crash.
- La cabecera muestra el disco en vivo.
- Nada se modifica sin confirmación.
