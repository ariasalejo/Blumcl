# 🚀 BLUMCL

**Observar → Analizar → Comprender → Recomendar → Confirmar → Actuar**

Herramienta local para Termux/Android de diagnóstico, análisis y
limpieza controlada del sistema, con IA 100% local y privada.

> Blumcl no limpia por limpiar: te ayuda a comprender tu dispositivo.

## ✨ Características

- 🔬 Escáner de almacenamiento que observa sin modificar
- 🛡️ Zonas intocables configurables (nunca toca lo crítico)
- ⏳ Snapshots con marca de tiempo: reconstrucción cronológica
- 📊 Informe HTML autocontenido (offline, sin CDNs)
- 🤖 IA local privada (llama.cpp) que interpreta tu evidencia
- 🧹 Limpieza controlada con dry-run y confirmación humana
- 🎛️ Terminal responsiva con banner cyan y robot guía
- 🚫 Cero nube · cero cuentas · cero telemetría

## 📱 Instalación

    pkg install python git
    git clone https://github.com/ariasalejo/Blumcl.git && cd Blumcl
    blumcl

## 🎛️ Uso

    blumcl
    → 1  escanear y guardar snapshot
    → 2  generar y descargar informe
    → 3  comparar snapshots (qué cambió)
    → 5  preguntar a la IA local
    → 7  limpieza dry-run (solo sugerencias)

## 🔐 Seguridad

Ver docs/security/principles.md.
El análisis nunca modifica. Nada se borra sin confirmación.
Los informes personales no se publican (reports/ en .gitignore).

## 🗺️ Arquitectura

Ver docs/architecture/overview.md y docs/architecture/flow.md.

## 🎁 Por qué existe este repo

Blumcl es un regalo de Blumix para la gente: la prueba de que se
puede aprender ingeniería de verdad construyendo desde un celular.
Hecho con ❤️ en Medellín.

## 🚧 Estado

v0.5.1 · desarrollo activo · construido en un teléfono

## 📦 Dependencias

```text
(ninguna — 100% librería estándar de Python)
```

## ⚡ Instalación en 4 líneas

```bash
pkg install git python
git clone https://github.com/ariasalejo/Blumcl.git
cd Blumcl && bash install.sh
blumcl
```

El instalador crea el comando global `blumcl` (wrapper en `$PREFIX/bin`).
🤖 IA local opcional: `pkg install llama.cpp` + modelo (~1.1 GB). Blumcl funciona 100% sin ella.
