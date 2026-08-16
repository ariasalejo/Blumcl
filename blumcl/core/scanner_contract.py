"""
BLUMCL · Contrato común para scanners.

Un scanner:
    observa
    recopila
    estructura

Un scanner NO:
    elimina
    modifica
    ejecuta acciones destructivas
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ScanResult:
    """
    Resultado normalizado de cualquier scanner BLUMCL.
    """

    scanner: str

    started_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    finished_at: str | None = None

    status: str = "ok"

    observations: dict[str, Any] = field(
        default_factory=dict
    )

    evidence: list[dict[str, Any]] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    def finalizar(self) -> None:
        self.finished_at = datetime.now(
            timezone.utc
        ).isoformat()

    def add_warning(self, mensaje: str) -> None:
        self.warnings.append(str(mensaje))

    def add_error(self, mensaje: str) -> None:
        self.errors.append(str(mensaje))
        self.status = "error"

    def to_dict(self) -> dict[str, Any]:
        return {
            "scanner": self.scanner,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "status": self.status,
            "observations": self.observations,
            "evidence": self.evidence,
            "warnings": self.warnings,
            "errors": self.errors,
        }
