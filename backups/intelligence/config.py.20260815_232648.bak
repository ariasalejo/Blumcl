"""
BLUMCL · Intelligence Configuration
===================================

Configuración centralizada del motor de inteligencia.

Flujo:

    Configuración
          ↓
    Reglas / Correlación
          ↓
      Evidencia
          ↓
       Señales
          ↓
      Prioridad

Este módulo:

    ✓ Lee TOML / JSON
    ✓ Normaliza la configuración
    ✓ Proporciona configuración tipada
    ✓ Proporciona configuración como diccionario
    ✓ No modifica archivos del usuario
    ✓ No ejecuta acciones de limpieza

Copyright © 2026 Eduar Alejandro Arias Londoño
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping
import json
import tomllib


__author__ = "Eduar Alejandro Arias Londoño"
__copyright__ = "Copyright © 2026 Eduar Alejandro Arias Londoño"
__license__ = "MIT"
__version__ = "1.2.0"


__all__ = [
    "IntelligenceConfig",
    "DEFAULT_CONFIG",
    "default_config",
    "config_to_dict",
    "config_from_dict",
    "load_config",
    "get_config",
    "get_typed_config",
    "describe_config",
]


# ============================================================
# SEVERITY
# ============================================================

DEFAULT_SEVERITY_WEIGHTS: Mapping[str, int] = {
    "critical": 100,
    "high": 80,
    "warning": 60,
    "review": 30,
    "info": 10,
}


# ============================================================
# HELPERS
# ============================================================

def _norm_str_tuple(value: Any) -> tuple[str, ...]:
    """
    Normaliza una lista, tupla o string a una tupla de strings.

    Ejemplos:

        ["Cache", "TMP"]
        →
        ("cache", "tmp")

        "cache,tmp"
        →
        ("cache", "tmp")
    """

    if value is None:
        return ()

    if isinstance(value, str):
        items = value.split(",")

    elif isinstance(value, (list, tuple)):
        items = list(value)

    else:
        items = [value]

    return tuple(
        str(item).strip().lower()
        for item in items
        if str(item).strip()
    )


def _normalize_size_tiers(
    value: Any,
) -> tuple[tuple[int, int], ...]:
    """
    Normaliza los niveles de tamaño.

    TOML puede entregar:

        [
            [104857600, 10],
            [524288000, 20],
        ]

    y se convierte a:

        (
            (104857600, 10),
            (524288000, 20),
        )
    """

    if value is None:
        return ()

    result: list[tuple[int, int]] = []

    try:
        for item in value:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                result.append(
                    (
                        int(item[0]),
                        int(item[1]),
                    )
                )
    except (TypeError, ValueError):
        return ()

    return tuple(result)


def _copy_mapping(
    value: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """
    Copia un Mapping a dict normal.
    """

    if not isinstance(value, Mapping):
        return {}

    return dict(value)


# ============================================================
# CONFIGURATION DATACLASS
# ============================================================

@dataclass(frozen=True)
class IntelligenceConfig:
    """
    Configuración completa del motor de inteligencia.
    """

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    schema_version: str = "1.1.0"

    # --------------------------------------------------------
    # SIZES
    # --------------------------------------------------------

    large_file_bytes: int = 100 * 1024 * 1024

    size_bonus_tiers: tuple[tuple[int, int], ...] = (
        (100 * 1024 * 1024, 10),
        (500 * 1024 * 1024, 20),
        (1024 * 1024 * 1024, 30),
        (5 * 1024 * 1024 * 1024, 40),
    )

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    old_file_days: int = 180

    stale_temp_days: int = 30

    stale_cache_days: int = 30

    old_download_days: int = 90

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence_min: float = 0.30

    confidence_low_threshold: float = 0.50

    confidence_high_threshold: float = 0.85

    # --------------------------------------------------------
    # RECURRENCE
    # --------------------------------------------------------

    recurrence_step: int = 5

    recurrence_cap: int = 15

    persistence_threshold: int = 2

    # --------------------------------------------------------
    # TRENDS
    # --------------------------------------------------------

    growth_threshold_bytes: int = 1024 * 1024

    growth_percent_threshold: float = 10.0

    burst_occurrences: int = 3

    abnormal_growth_factor: float = 3.0

    # --------------------------------------------------------
    # LIMITS
    # --------------------------------------------------------

    max_snapshots: int = 1000

    max_evidence_per_snapshot: int = 100_000

    max_path_length: int = 4096

    # --------------------------------------------------------
    # PATHS
    # --------------------------------------------------------

    snapshots_dir: Path = Path("data/snapshots")

    reports_dir: Path = Path("reports")

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    ignore_path_fragments: tuple[str, ...] = ()

    include_path_fragments: tuple[str, ...] = ()

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    top: int = 20

    output_format: str = "table"

    sort_by: str = "priority"

    # --------------------------------------------------------
    # BEHAVIOR
    # --------------------------------------------------------

    enable_derived_signals: bool = True

    allow_dynamic_rules: bool = False

    # --------------------------------------------------------
    # SCORING
    # --------------------------------------------------------

    confidence_bonus_max: int = 10

    recurrence_bonus_max: int = 15

    persistence_bonus_max: int = 15

    trend_bonus_max: int = 10

    size_bonus_max: int = 40

    max_priority: int = 100

    severity_weights: Mapping[str, int] = field(
        default_factory=lambda: dict(
            DEFAULT_SEVERITY_WEIGHTS
        )
    )


# ============================================================
# DEFAULT CONFIG
# ============================================================

DEFAULT_CONFIG = IntelligenceConfig()


def default_config() -> IntelligenceConfig:
    """
    Devuelve la configuración predeterminada.
    """

    return DEFAULT_CONFIG


# ============================================================
# CONFIG FROM DICT
# ============================================================

def config_from_dict(
    data: Mapping[str, Any],
) -> IntelligenceConfig:
    """
    Construye IntelligenceConfig desde TOML o JSON.

    El archivo utiliza secciones:

        [general]
        [sizes]
        [time]
        [confidence]
        [recurrence]
        [trends]
        [limits]
        [paths]
        [filters]
        [report]
        [behavior]
        [scoring]
        [scoring.severity_weights]

    IntelligenceConfig utiliza nombres planos.
    """

    if not isinstance(data, Mapping):
        raise TypeError(
            "La configuración debe ser un Mapping."
        )

    def _section(
        name: str,
    ) -> Mapping[str, Any]:

        value = data.get(
            name,
            {},
        )

        if isinstance(value, Mapping):
            return value

        return {}

    def _get(
        section: str,
        key: str,
        default: Any,
    ) -> Any:

        return _section(section).get(
            key,
            default,
        )

    # --------------------------------------------------------
    # SEVERITY
    # --------------------------------------------------------

    severity_weights = _get(
        "scoring",
        "severity_weights",
        dict(DEFAULT_SEVERITY_WEIGHTS),
    )

    if not isinstance(
        severity_weights,
        Mapping,
    ):
        severity_weights = dict(
            DEFAULT_SEVERITY_WEIGHTS
        )

    severity_weights = {
        str(key): int(value)
        for key, value in severity_weights.items()
    }

    # --------------------------------------------------------
    # SIZE TIERS
    # --------------------------------------------------------

    size_bonus_tiers = _normalize_size_tiers(
        _get(
            "sizes",
            "size_bonus_tiers",
            DEFAULT_CONFIG.size_bonus_tiers,
        )
    )

    if not size_bonus_tiers:
        size_bonus_tiers = DEFAULT_CONFIG.size_bonus_tiers

    # --------------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------------

    return IntelligenceConfig(

        # ----------------------------------------------------
        # GENERAL
        # ----------------------------------------------------

        schema_version=str(
            _get(
                "general",
                "schema_version",
                "1.1.0",
            )
        ),

        # ----------------------------------------------------
        # SIZES
        # ----------------------------------------------------

        large_file_bytes=int(
            _get(
                "sizes",
                "large_file_bytes",
                100 * 1024 * 1024,
            )
        ),

        size_bonus_tiers=size_bonus_tiers,

        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        old_file_days=int(
            _get(
                "time",
                "old_file_days",
                180,
            )
        ),

        stale_temp_days=int(
            _get(
                "time",
                "stale_temp_days",
                30,
            )
        ),

        stale_cache_days=int(
            _get(
                "time",
                "stale_cache_days",
                30,
            )
        ),

        old_download_days=int(
            _get(
                "time",
                "old_download_days",
                90,
            )
        ),

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        confidence_min=float(
            _get(
                "confidence",
                "min_confidence",
                0.30,
            )
        ),

        confidence_low_threshold=float(
            _get(
                "confidence",
                "low_confidence_threshold",
                0.50,
            )
        ),

        confidence_high_threshold=float(
            _get(
                "confidence",
                "high_confidence_threshold",
                0.85,
            )
        ),

        # ----------------------------------------------------
        # RECURRENCE
        # ----------------------------------------------------

        recurrence_step=int(
            _get(
                "recurrence",
                "recurrence_step",
                5,
            )
        ),

        recurrence_cap=int(
            _get(
                "recurrence",
                "recurrence_cap",
                15,
            )
        ),

        persistence_threshold=int(
            _get(
                "recurrence",
                "persistence_threshold",
                2,
            )
        ),

        # ----------------------------------------------------
        # TRENDS
        # ----------------------------------------------------

        growth_threshold_bytes=int(
            _get(
                "trends",
                "growth_threshold_bytes",
                1024 * 1024,
            )
        ),

        growth_percent_threshold=float(
            _get(
                "trends",
                "growth_percent_threshold",
                10.0,
            )
        ),

        burst_occurrences=int(
            _get(
                "trends",
                "burst_occurrences",
                3,
            )
        ),

        abnormal_growth_factor=float(
            _get(
                "trends",
                "abnormal_growth_factor",
                3.0,
            )
        ),

        # ----------------------------------------------------
        # LIMITS
        # ----------------------------------------------------

        max_snapshots=int(
            _get(
                "limits",
                "max_snapshots",
                1000,
            )
        ),

        max_evidence_per_snapshot=int(
            _get(
                "limits",
                "max_evidence_per_snapshot",
                100_000,
            )
        ),

        max_path_length=int(
            _get(
                "limits",
                "max_path_length",
                4096,
            )
        ),

        # ----------------------------------------------------
        # PATHS
        # ----------------------------------------------------

        snapshots_dir=Path(
            _get(
                "paths",
                "snapshots_dir",
                "data/snapshots",
            )
        ),

        reports_dir=Path(
            _get(
                "paths",
                "reports_dir",
                "reports",
            )
        ),

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        ignore_path_fragments=_norm_str_tuple(
            _get(
                "filters",
                "ignore_path_fragments",
                (),
            )
        ),

        include_path_fragments=_norm_str_tuple(
            _get(
                "filters",
                "include_path_fragments",
                (),
            )
        ),

        # ----------------------------------------------------
        # REPORT
        # ----------------------------------------------------

        top=int(
            _get(
                "report",
                "top",
                20,
            )
        ),

        output_format=str(
            _get(
                "report",
                "output_format",
                "table",
            )
        ),

        sort_by=str(
            _get(
                "report",
                "sort_by",
                "priority",
            )
        ),

        # ----------------------------------------------------
        # BEHAVIOR
        # ----------------------------------------------------

        enable_derived_signals=bool(
            _get(
                "behavior",
                "enable_derived_signals",
                True,
            )
        ),

        allow_dynamic_rules=bool(
            _get(
                "behavior",
                "allow_dynamic_rules",
                False,
            )
        ),

        # ----------------------------------------------------
        # SCORING
        # ----------------------------------------------------

        confidence_bonus_max=int(
            _get(
                "scoring",
                "confidence_bonus_max",
                10,
            )
        ),

        recurrence_bonus_max=int(
            _get(
                "scoring",
                "recurrence_bonus_max",
                15,
            )
        ),

        persistence_bonus_max=int(
            _get(
                "scoring",
                "persistence_bonus_max",
                15,
            )
        ),

        trend_bonus_max=int(
            _get(
                "scoring",
                "trend_bonus_max",
                10,
            )
        ),

        size_bonus_max=int(
            _get(
                "scoring",
                "size_bonus_max",
                40,
            )
        ),

        max_priority=int(
            _get(
                "scoring",
                "max_priority",
                100,
            )
        ),

        severity_weights=severity_weights,
    )


# ============================================================
# CONFIG TO DICT
# ============================================================

def config_to_dict(
    config: IntelligenceConfig = DEFAULT_CONFIG,
) -> dict[str, Any]:
    """
    Convierte IntelligenceConfig a un diccionario estructurado.

    Esta estructura coincide con el TOML.
    """

    return {
        "general": {
            "schema_version": config.schema_version,
        },

        "sizes": {
            "large_file_bytes": config.large_file_bytes,
            "size_bonus_tiers": [
                list(item)
                for item in config.size_bonus_tiers
            ],
        },

        "time": {
            "old_file_days": config.old_file_days,
            "stale_temp_days": config.stale_temp_days,
            "stale_cache_days": config.stale_cache_days,
            "old_download_days": config.old_download_days,
        },

        "confidence": {
            "min_confidence": config.confidence_min,
            "low_confidence_threshold": (
                config.confidence_low_threshold
            ),
            "high_confidence_threshold": (
                config.confidence_high_threshold
            ),
        },

        "recurrence": {
            "recurrence_step": config.recurrence_step,
            "recurrence_cap": config.recurrence_cap,
            "persistence_threshold": (
                config.persistence_threshold
            ),
        },

        "trends": {
            "growth_threshold_bytes": (
                config.growth_threshold_bytes
            ),
            "growth_percent_threshold": (
                config.growth_percent_threshold
            ),
            "burst_occurrences": config.burst_occurrences,
            "abnormal_growth_factor": (
                config.abnormal_growth_factor
            ),
        },

        "limits": {
            "max_snapshots": config.max_snapshots,
            "max_evidence_per_snapshot": (
                config.max_evidence_per_snapshot
            ),
            "max_path_length": config.max_path_length,
        },

        "paths": {
            "snapshots_dir": str(
                config.snapshots_dir
            ),
            "reports_dir": str(
                config.reports_dir
            ),
        },

        "filters": {
            "ignore_path_fragments": list(
                config.ignore_path_fragments
            ),
            "include_path_fragments": list(
                config.include_path_fragments
            ),
        },

        "report": {
            "top": config.top,
            "output_format": config.output_format,
            "sort_by": config.sort_by,
        },

        "behavior": {
            "enable_derived_signals": (
                config.enable_derived_signals
            ),
            "allow_dynamic_rules": (
                config.allow_dynamic_rules
            ),
        },

        "scoring": {
            "confidence_bonus_max": (
                config.confidence_bonus_max
            ),
            "recurrence_bonus_max": (
                config.recurrence_bonus_max
            ),
            "persistence_bonus_max": (
                config.persistence_bonus_max
            ),
            "trend_bonus_max": config.trend_bonus_max,
            "size_bonus_max": config.size_bonus_max,
            "max_priority": config.max_priority,
            "severity_weights": dict(
                config.severity_weights
            ),
        },
    }


# ============================================================
# LOAD CONFIG
# ============================================================

def load_config(
    path: str | Path | None = None,
) -> IntelligenceConfig:
    """
    Carga configuración desde TOML o JSON.

    Si no existe el archivo:

        config/blumcl.toml

    se utiliza DEFAULT_CONFIG.
    """

    candidate = (
        Path(path).expanduser()
        if path
        else Path("config/blumcl.toml")
    )

    if not candidate.exists():
        return default_config()

    try:

        if candidate.suffix.lower() == ".json":

            data = json.loads(
                candidate.read_text(
                    encoding="utf-8"
                )
            )

        else:

            data = tomllib.loads(
                candidate.read_text(
                    encoding="utf-8"
                )
            )

    except Exception as exc:

        raise ValueError(
            f"No se pudo leer la configuración: "
            f"{candidate}"
        ) from exc

    return config_from_dict(data)


# ============================================================
# DICTIONARY API
# ============================================================

def get_config(
    path: str | Path | None = None,
) -> dict[str, Any]:
    """
    API compatible para obtener la configuración
    como diccionario estructurado.

    Ejemplo:

        cfg = get_config()

        cfg["limits"]["max_evidence_per_snapshot"]
        cfg["sizes"]["large_file_bytes"]
        cfg["confidence"]
        cfg["trends"]
    """

    config = load_config(path)

    return config_to_dict(config)


# ============================================================
# TYPED API
# ============================================================

def get_typed_config(
    path: str | Path | None = None,
) -> IntelligenceConfig:
    """
    Devuelve la configuración tipada.
    """

    return load_config(path)


# ============================================================
# DESCRIPTION
# ============================================================

def describe_config(
    config: IntelligenceConfig = DEFAULT_CONFIG,
) -> str:
    """
    Devuelve una representación legible.
    """

    values = config_to_dict(config)

    lines = [
        "🧠 BLUMCL · INTELLIGENCE CONFIGURATION",
        "=" * 64,
    ]

    for section, values_section in values.items():

        lines.append("")
        lines.append(
            f"[{section}]"
        )

        if isinstance(
            values_section,
            Mapping,
        ):

            for key, value in values_section.items():

                if isinstance(
                    value,
                    (list, tuple, dict),
                ):
                    text = json.dumps(
                        value,
                        ensure_ascii=False,
                    )

                else:
                    text = str(value)

                lines.append(
                    f"{key:32} {text}"
                )

    return "\n".join(lines)


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    cfg = load_config()

    print(
        describe_config(cfg)
    )

    print()
    print("✅ IntelligenceConfig OK")
    print(
        "📦 max_evidence:",
        cfg.max_evidence_per_snapshot,
    )
    print(
        "📁 large_file_bytes:",
        cfg.large_file_bytes,
    )
    print(
        "🎯 confidence:",
        cfg.confidence_min,
        cfg.confidence_low_threshold,
        cfg.confidence_high_threshold,
    )
    print(
        "📈 growth:",
        cfg.growth_percent_threshold,
    )
