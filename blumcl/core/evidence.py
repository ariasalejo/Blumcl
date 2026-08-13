"""
BLUMCL - Evidence Core

Modelo central de evidencia para BLUMCL.

Principios:
    - La observación se separa de la interpretación.
    - La IA no tiene autoridad para ejecutar acciones.
    - La evidencia debe ser auditable.
    - Las acciones destructivas nunca son implícitas.
    - El modelo debe poder evolucionar sin romper datos existentes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable
import json
import os


class EvidenceCategory(str, Enum):
    """Clasificación comprensible para el usuario."""

    PROTECTED = "protected"
    IMPORTANT = "important"
    REVIEW = "review"
    POSSIBLE_DUPLICATE = "possible_duplicate"
    QUARANTINE_CANDIDATE = "quarantine_candidate"


class EvidenceAction(str, Enum):
    """Acciones posibles sobre una evidencia."""

    NONE = "none"
    REVIEW = "review"
    QUARANTINE = "quarantine"
    RESTORE = "restore"


class EvidenceSource(str, Enum):
    """Origen de la observación."""

    STORAGE_SCANNER = "storage_scanner"
    MEMORY_SCANNER = "memory_scanner"
    CPU_SCANNER = "cpu_scanner"
    SYSTEM_SCANNER = "system_scanner"
    APPS_SCANNER = "apps_scanner"
    ANALYSIS_ENGINE = "analysis_engine"
    USER = "user"


@dataclass(frozen=True)
class EvidenceReason:
    """Explicación individual de por qué existe un hallazgo."""

    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "message": self.message,
        }


@dataclass
class Evidence:
    """
    Unidad principal de evidencia de BLUMCL.

    Importante:
        Evidence describe lo observado y el análisis asociado.
        No ejecuta operaciones sobre el sistema.
    """

    evidence_id: str
    timestamp: str
    path: str

    source: EvidenceSource = EvidenceSource.ANALYSIS_ENGINE
    category: EvidenceCategory = EvidenceCategory.REVIEW

    size_bytes: int | None = None
    file_type: str | None = None

    reasons: list[EvidenceReason] = field(default_factory=list)

    confidence: float | None = None

    sha256: str | None = None
    snapshot_id: str | None = None

    recommendation: str | None = None
    action: EvidenceAction = EvidenceAction.NONE

    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Valida invariantes básicas del modelo."""

        if not self.evidence_id.startswith("BLUMCL-E-"):
            raise ValueError(
                "evidence_id debe comenzar con 'BLUMCL-E-'"
            )

        if not self.path:
            raise ValueError("path no puede estar vacío")

        if self.size_bytes is not None and self.size_bytes < 0:
            raise ValueError("size_bytes no puede ser negativo")

        if self.confidence is not None:
            if not 0.0 <= self.confidence <= 1.0:
                raise ValueError(
                    "confidence debe estar entre 0.0 y 1.0"
                )

        if self.sha256 is not None:
            normalized_hash = self.sha256.lower()

            if len(normalized_hash) != 64:
                raise ValueError(
                    "sha256 debe contener 64 caracteres hexadecimales"
                )

            if any(
                character not in "0123456789abcdef"
                for character in normalized_hash
            ):
                raise ValueError(
                    "sha256 contiene caracteres inválidos"
                )

            self.sha256 = normalized_hash

    @staticmethod
    def create_id(sequence: int) -> str:
        """
        Crea un identificador legible y estable.

        Ejemplo:
            BLUMCL-E-000042
        """

        if sequence < 0:
            raise ValueError("sequence no puede ser negativo")

        return f"BLUMCL-E-{sequence:06d}"

    @staticmethod
    def now() -> str:
        """Devuelve una marca temporal UTC en formato ISO-8601."""

        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def create(
        cls,
        *,
        sequence: int,
        path: str | Path,
        source: EvidenceSource,
        category: EvidenceCategory = EvidenceCategory.REVIEW,
        size_bytes: int | None = None,
        file_type: str | None = None,
        reasons: Iterable[EvidenceReason] | None = None,
        confidence: float | None = None,
        snapshot_id: str | None = None,
        recommendation: str | None = None,
        action: EvidenceAction = EvidenceAction.NONE,
        metadata: dict[str, Any] | None = None,
    ) -> "Evidence":
        """Constructor de alto nivel para crear evidencia."""

        return cls(
            evidence_id=cls.create_id(sequence),
            timestamp=cls.now(),
            path=os.fspath(path),
            source=source,
            category=category,
            size_bytes=size_bytes,
            file_type=file_type,
            reasons=list(reasons or []),
            confidence=confidence,
            snapshot_id=snapshot_id,
            recommendation=recommendation,
            action=action,
            metadata=dict(metadata or {}),
        )

    def add_reason(self, code: str, message: str) -> None:
        """Añade una razón al hallazgo."""

        if not code:
            raise ValueError("code no puede estar vacío")

        if not message:
            raise ValueError("message no puede estar vacío")

        self.reasons.append(
            EvidenceReason(
                code=code,
                message=message,
            )
        )

    def has_reasons(self) -> bool:
        """Indica si existe evidencia explicativa."""

        return bool(self.reasons)

    def set_hash(self, digest: str) -> None:
        """Asocia un SHA-256 previamente calculado."""

        digest = digest.lower()

        if len(digest) != 64:
            raise ValueError("SHA-256 inválido")

        int(digest, 16)

        self.sha256 = digest

    def to_dict(self) -> dict[str, Any]:
        """Serializa la evidencia a un diccionario seguro."""

        data = asdict(self)

        data["source"] = self.source.value
        data["category"] = self.category.value
        data["action"] = self.action.value

        data["reasons"] = [
            reason.to_dict()
            for reason in self.reasons
        ]

        return data

    def to_json(self, *, indent: int = 2) -> str:
        """Serializa la evidencia a JSON."""

        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
            sort_keys=True,
        )


def calculate_sha256(
    path: str | Path,
    *,
    chunk_size: int = 1024 * 1024,
) -> str:
    """
    Calcula SHA-256 de un archivo de forma incremental.

    No carga el archivo completo en memoria.
    """

    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"No existe un archivo regular: {file_path}"
        )

    if chunk_size <= 0:
        raise ValueError("chunk_size debe ser mayor que cero")

    digest = sha256()

    with file_path.open("rb") as file:
        while True:
            chunk = file.read(chunk_size)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def evidence_from_file(
    *,
    sequence: int,
    path: str | Path,
    source: EvidenceSource,
    category: EvidenceCategory = EvidenceCategory.REVIEW,
    calculate_hash: bool = False,
    snapshot_id: str | None = None,
) -> Evidence:
    """
    Crea evidencia básica a partir de un archivo existente.

    La función solamente observa el archivo.
    No modifica, mueve ni elimina nada.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"No existe la ruta: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"La ruta no corresponde a un archivo: {file_path}"
        )

    stat = file_path.stat()

    evidence = Evidence.create(
        sequence=sequence,
        path=file_path,
        source=source,
        category=category,
        size_bytes=stat.st_size,
        file_type=file_path.suffix.lower() or None,
        snapshot_id=snapshot_id,
    )

    if calculate_hash:
        evidence.set_hash(
            calculate_sha256(file_path)
        )

    return evidence


__all__ = [
    "Evidence",
    "EvidenceAction",
    "EvidenceCategory",
    "EvidenceReason",
    "EvidenceSource",
    "calculate_sha256",
    "evidence_from_file",
]
