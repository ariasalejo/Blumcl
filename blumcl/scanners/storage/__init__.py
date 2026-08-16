"""BLUMCL · Storage Scanner.

API pública del scanner de almacenamiento.

El módulo ``scanner.py`` contiene la implementación.
Este archivo expone únicamente las funciones que deben
ser utilizadas por el resto de BLUMCL.

Principio:

    observar → analizar → evidenciar → snapshot

El scanner nunca elimina ni mueve archivos.
"""

from .scanner import (
    analizar,
    analizar_snapshot,
    archivos_grandes,
    autodiagnostico,
    crear_snapshot,
    espacio,
    generar_evidencias_archivos_grandes,
    guardar_snapshot,
    guardar_snapshot_oficial,
)


__all__ = [
    "analizar",
    "analizar_snapshot",
    "archivos_grandes",
    "autodiagnostico",
    "crear_snapshot",
    "espacio",
    "generar_evidencias_archivos_grandes",
    "guardar_snapshot",
    "guardar_snapshot_oficial",
]
