"""
BLUMCL - CPU Scanner.

Observación segura de información básica del procesador.

Principios:
    - Solo observa.
    - No modifica el sistema.
    - No ejecuta acciones destructivas.
    - Devuelve datos estructurados.
"""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CPUInfo:
    """Información observada del procesador."""

    architecture: str
    processor: str
    logical_cpus: int

    def __post_init__(self) -> None:
        """Valida la observación antes de aceptarla."""

        if not self.architecture.strip():
            raise ValueError("architecture no puede estar vacía")

        if not self.processor.strip():
            raise ValueError("processor no puede estar vacío")

        if self.logical_cpus <= 0:
            raise ValueError(
                "logical_cpus debe ser mayor que cero"
            )

    def to_dict(self) -> dict[str, object]:
        """Convierte la observación a un diccionario."""

        return {
            "architecture": self.architecture,
            "processor": self.processor,
            "logical_cpus": self.logical_cpus,
        }


def scan() -> CPUInfo:
    """
    Observa información básica de la CPU.

    La función solamente consulta información disponible
    mediante la biblioteca estándar de Python.
    """

    architecture = platform.machine() or "unknown"
    processor = platform.processor() or "unknown"
    logical_cpus = os.cpu_count() or 1

    return CPUInfo(
        architecture=architecture,
        processor=processor,
        logical_cpus=logical_cpus,
    )


__all__ = [
    "CPUInfo",
    "scan",
]
