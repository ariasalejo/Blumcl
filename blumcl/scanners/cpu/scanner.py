"""
BLUMCL - CPU Scanner.

Observación segura de información básica del procesador.

Principios:
    - Solo observa.
    - No modifica el sistema.
    - No ejecuta acciones destructivas.
    - Devuelve datos estructurados.
    - Puede convertir la observación en Evidence auditable.
"""

from __future__ import annotations

import os
import platform
from dataclasses import dataclass

from blumcl.core.evidence import (
    Evidence,
    EvidenceCategory,
    EvidenceSource,
)


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


def generar_evidencia_cpu(
    info: CPUInfo,
    *,
    sequence: int,
    snapshot_id: str | None = None,
) -> Evidence:
    """
    Convierte una observación CPU en Evidence auditable.

    Esta función NO modifica el sistema.
    Solamente transforma datos observados en el modelo
    central de evidencia de BLUMCL.
    """

    evidence = Evidence.create(
        sequence=sequence,
        path="cpu://local",
        source=EvidenceSource.CPU_SCANNER,
        category=EvidenceCategory.REVIEW,
        snapshot_id=snapshot_id,
        recommendation="Revisar la información observada de la CPU.",
        metadata={
            "architecture": info.architecture,
            "processor": info.processor,
            "logical_cpus": info.logical_cpus,
        },
    )

    evidence.add_reason(
        "CPU_OBSERVED",
        (
            f"CPU observada: arquitectura={info.architecture}, "
            f"procesador={info.processor}, "
            f"CPUs lógicas={info.logical_cpus}."
        ),
    )

    return evidence


__all__ = [
    "CPUInfo",
    "generar_evidencia_cpu",
    "scan",
]
