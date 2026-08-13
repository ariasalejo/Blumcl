"""
BLUMCL · Diagnostic Engine

Motor central de diagnóstico.

Flujo:

    Scanner
       ↓
    Observación
       ↓
    Evidence
       ↓
    DiagnosticResult
       ↓
    Snapshot / Report / IA

Principios:

    • Observar antes de actuar.
    • Evidencia antes que opinión.
    • La IA interpreta, no ejecuta.
    • Ninguna operación destructiva pertenece aquí.
    • Los scanners permanecen independientes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from blumcl.core.evidence import Evidence


@dataclass
class DiagnosticResult:
    """
    Resultado completo de una ejecución diagnóstica.

    No realiza modificaciones sobre el sistema.
    """

    diagnostic_id: str
    timestamp: str
    evidence: list[Evidence] = field(default_factory=list)
    observations: dict[str, Any] = field(default_factory=dict)
    scanners: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def evidence_count(self) -> int:
        """Cantidad de evidencias generadas."""
        return len(self.evidence)

    @property
    def scanner_count(self) -> int:
        """Cantidad de scanners ejecutados."""
        return len(self.scanners)

    def to_dict(self) -> dict[str, Any]:
        """Convierte el resultado a un diccionario serializable."""
        return {
            "diagnostic_id": self.diagnostic_id,
            "timestamp": self.timestamp,
            "evidence": [
                evidence.to_dict()
                for evidence in self.evidence
            ],
            "observations": self.observations,
            "scanners": self.scanners,
            "metadata": self.metadata,
        }


class DiagnosticEngine:
    """
    Orquestador principal de diagnóstico de BLUMCL.

    Integra actualmente:

        • Storage Scanner
        • CPU Scanner

    Los demás scanners podrán añadirse posteriormente sin
    modificar el contrato central de Evidence.
    """

    VERSION = "0.1.0"

    def __init__(self) -> None:
        self._sequence = 0

    # ---------------------------------------------------------
    # IDENTIFICACIÓN
    # ---------------------------------------------------------

    @staticmethod
    def _diagnostic_id() -> str:
        """
        Genera un identificador único para la ejecución.

        Ejemplo:

            BLUMCL-D-20260813-183429
        """

        now = datetime.now(timezone.utc)

        return (
            "BLUMCL-D-"
            f"{now.strftime('%Y%m%d-%H%M%S')}"
        )

    # ---------------------------------------------------------
    # SECUENCIA DE EVIDENCIAS
    # ---------------------------------------------------------

    def _next_sequence(self) -> int:
        """Obtiene el siguiente número de evidencia."""
        self._sequence += 1
        return self._sequence

    # ---------------------------------------------------------
    # CPU
    # ---------------------------------------------------------

    def _scan_cpu(
        self,
        result: DiagnosticResult,
    ) -> None:
        """
        Ejecuta el CPU Scanner y genera su evidencia.

        Si el scanner falla, el diagnóstico completo no se
        detiene. El error queda registrado como estado del scanner.
        """

        scanner_name = "cpu"

        try:
            from blumcl.scanners.cpu.scanner import (
                scan,
                generar_evidencia_cpu,
            )

            # -------------------------------------------------
            # Observación
            # -------------------------------------------------

            cpu_data = scan()

            result.observations["cpu"] = cpu_data
            result.scanners[scanner_name] = "ok"

            # -------------------------------------------------
            # Evidencia
            # -------------------------------------------------

            evidence = generar_evidencia_cpu(
                cpu_data,
                sequence=self._next_sequence(),
            )

            result.evidence.append(evidence)

        except Exception as exc:
            result.scanners[scanner_name] = "error"

            result.metadata.setdefault(
                "errors",
                [],
            ).append(
                {
                    "scanner": scanner_name,
                    "error": str(exc),
                }
            )

    # ---------------------------------------------------------
    # STORAGE
    # ---------------------------------------------------------

    def _scan_storage(
        self,
        result: DiagnosticResult,
    ) -> None:
        """
        Ejecuta el Storage Scanner.

        Esta integración conserva el comportamiento existente
        de BLUMCL y todavía no reemplaza el flujo histórico
        de snapshots.
        """

        scanner_name = "storage"

        try:
            from blumcl.scanners.storage import scanner

            storage_data = scanner.analizar()

            result.observations["storage"] = storage_data
            result.scanners[scanner_name] = "ok"

        except Exception as exc:
            result.scanners[scanner_name] = "error"

            result.metadata.setdefault(
                "errors",
                [],
            ).append(
                {
                    "scanner": scanner_name,
                    "error": str(exc),
                }
            )

    # ---------------------------------------------------------
    # EJECUCIÓN PRINCIPAL
    # ---------------------------------------------------------

    def ejecutar(
        self,
        *,
        incluir_storage: bool = True,
        incluir_cpu: bool = True,
    ) -> DiagnosticResult:
        """
        Ejecuta una ronda de diagnóstico.

        Por defecto:

            Storage = sí
            CPU     = sí

        Ningún scanner ejecutado por este método debe realizar
        modificaciones destructivas.
        """

        timestamp = datetime.now(timezone.utc).isoformat()

        result = DiagnosticResult(
            diagnostic_id=self._diagnostic_id(),
            timestamp=timestamp,
            metadata={
                "engine": "BLUMCL Diagnostic Engine",
                "version": self.VERSION,
                "destructive_actions": False,
            },
        )

        if incluir_storage:
            self._scan_storage(result)

        if incluir_cpu:
            self._scan_cpu(result)

        return result
