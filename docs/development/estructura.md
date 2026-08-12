# 🗺️ BLUMCL · Mapa de carpetas

## Públicas (se ven en GitHub)
- blumcl/ → el motor Python
  - core/ → coordinación general (v0.5)
  - scanners/ → observar sin modificar
  - analysis/ → comparar e interpretar
  - cleaner/ → limpieza controlada (dry-run)
  - reports/ → generadores de informes
  - ai/ → puente con la IA local
  - ui/ → interfaz (v0.5)
  - utils/ → configuración y ayudas
- tests/ → una prueba por módulo
- docs/ → documentación pública
- config/ → protección y umbrales

## Privadas (locales por diseño, fuera de git)
- reports/ → informes con datos reales
- data/ → snapshots e historial
- logs/ → bitácora técnica

Regla: lo privado protege al usuario; lo público enseña al mundo.
