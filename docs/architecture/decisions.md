# 🧠 BLUMCL — Decisiones de Arquitectura

## Propósito

Este documento registra las decisiones técnicas importantes de Blumcl.

Blumcl debe evolucionar de forma controlada. Antes de introducir una
funcionalidad importante se debe comprender qué problema resuelve,
qué riesgos introduce y cómo afecta a la arquitectura.

---

## Decisión 001 — IA local sin autoridad de ejecución

**Estado:** 🟢 ACEPTADA

La IA local puede analizar información, explicar resultados y formular
recomendaciones.

La IA no ejecutará directamente operaciones sobre archivos.

La arquitectura será:

```text
EVIDENCIA
   ↓
IA
   ↓
RECOMENDACIÓN
   ↓
USUARIO
   ↓
CONFIRMACIÓN
   ↓
MÓDULO CONTROLADO
