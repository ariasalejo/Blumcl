# 🧠 BLUMCL — Arquitectura del Sistema

## 1. Visión

Blumcl es una herramienta local para Termux orientada al
diagnóstico, análisis y limpieza controlada del sistema.

Su propósito no es simplemente borrar archivos.

Blumcl debe ayudar al usuario a:

- observar el sistema;
- recopilar información;
- analizar recursos;
- identificar posibles residuos;
- comprender los hallazgos;
- generar informes;
- recibir asistencia de una IA local;
- decidir qué acciones realizar;
- ejecutar limpiezas controladas.

La filosofía fundamental es:

OBSERVAR → ANALIZAR → COMPRENDER → RECOMENDAR → CONFIRMAR → ACTUAR

---

## 2. Arquitectura general

```text
                         🧠 IA LOCAL
                             │
                             ▼
                    ┌─────────────────┐
                    │      BLUMCL     │
                    │ System Analysis │
                    └────────┬────────┘
                             │
        ┌────────────┬───────┼───────┬────────────┐
        ▼            ▼       ▼       ▼            ▼
     💾 DISCO      🧠 RAM   ⚙️ CPU  📦 APPS    🔐 SISTEMA
        │            │       │       │            │
        └────────────┴───────┼───────┴────────────┘
                             ▼
                       🔬 SCANNER
                             │
                             ▼
                       📊 EVIDENCIA
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                🤖 IA LOCAL       📋 INFORME
                    │                 │
                    └────────┬────────┘
                             ▼
                       🧹 LIMPIEZA CONTROLADA
```

## 3. Componentes principales

### 💾 Storage
Analiza el almacenamiento accesible: espacio total, utilizado y
disponible; archivos y directorios grandes; temporales; cachés;
descargas; posibles residuos.
El análisis no debe modificar archivos.

### 🧠 Memory
RAM utilizada y disponible; procesos; consumo; swap; zRAM.
Un proceso con mucha RAM no es automáticamente innecesario.

### ⚙️ CPU
Carga del procesador; procesos activos; consumo elevado;
información disponible del sistema.

### 📦 Apps
Aplicaciones; paquetes; tamaños; datos asociados; residuos.
Depende de los permisos disponibles en Android y Termux.

### 🔐 System
Versión de Android y Termux; arquitectura; kernel; permisos;
almacenamiento; herramientas disponibles; estado del entorno.

## 4. 🔬 Scanner

Primera regla: ANALIZAR SIN MODIFICAR.

📱 SISTEMA → 🔬 SCANNER → 📊 DATOS → 🧠 ANÁLISIS → 📋 EVIDENCIA

## 5. 📊 Evidencia

Los datos se conservan antes de actuar, para: revisar resultados,
comparar análisis, generar informes, alimentar la IA, conservar
historial y estudiar cambios del sistema.

## 6. 🤖 IA local

Ayuda a interpretar resultados, explicar conceptos, detectar
patrones, clasificar hallazgos, formular recomendaciones y
enseñar. No elimina archivos automáticamente.
La decisión final pertenece al usuario.

## 7. 📋 Informes

- **JSON**: datos estructurados (historial, comparación, IA).
- **HTML**: informe visual completo.
- **Imágenes**: gráficos de almacenamiento, RAM, CPU, apps y resumen.

Los informes pueden contener información privada y NO deben
subirse automáticamente al repositorio público.

## 8. 🧹 Limpieza controlada

🔬 DETECTAR → 🧠 ANALIZAR → 📋 EXPLICAR → 💡 RECOMENDAR →
👤 CONFIRMAR → 🧹 ACTUAR

Nunca eliminar algo solo porque sea grande, antiguo, de extensión
desconocida o esté en una carpeta poco conocida.

## 9. 🔐 Seguridad

- Analizar antes de modificar.
- Separar scanner y cleaner.
- Mostrar acciones antes de ejecutarlas.
- Solicitar confirmación.
- Evitar archivos críticos.
- No borrar arbitrariamente.
- No almacenar contraseñas ni claves privadas.
- No enviar datos privados sin consentimiento.
- Mantener resultados personales fuera del repo público.

## 10. 🔄 Flujo completo

```text
📱 TELÉFONO → 🚀 BLUMCL CORE → 🔬 SCANNER
→ 💾 DISCO / 🧠 RAM / ⚙️ CPU / 📦 APPS / 🔐 SISTEMA
→ 📊 EVIDENCIA → 🤖 IA LOCAL + 📋 INFORME
→ 💡 RECOMENDACIÓN → 👤 CONFIRMACIÓN → 🧹 CLEANER
→ 📊 INFORME FINAL
```

## 11. 🎯 Filosofía

Blumcl no debe limitarse a limpiar: debe ayudar al usuario a
comprender su dispositivo.

## 12. Estado del proyecto

- Proyecto: Blumcl · Versión: 0.1.0
- Plataforma objetivo: Termux / Android
- IA: local y opcional
- Limpieza automática: deshabilitada por defecto
- Informes visuales: previstos
- Documentación: en construcción
- Fecha: 2026-08-12
