"""BLUMCL · Storage Scanner.

Scanner profesional de almacenamiento.

Principios:
    - Observar sin modificar.
    - Generar evidencia estructurada.
    - Respetar rutas protegidas.
    - Integrar el Snapshot oficial de BLUMCL.
    - No eliminar ni mover archivos.
    - Mantener compatibilidad con el formato anterior.
    - Mostrar telemetría real durante el análisis.

Arquitectura:

    Storage Scanner
          ↓
    Observaciones
          ↓
       Evidence
          ↓
       Snapshot
          ↓
    Resultado normalizado

La función ``analizar()`` mantiene el formato histórico para
compatibilidad con código existente.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Any

from blumcl.core.evidence import (
    Evidence,
    EvidenceCategory,
    EvidenceSource,
    evidence_from_file,
)
from blumcl.core.snapshot import Snapshot
from blumcl.utils.config import cargar


HOME = Path.home()
RAIZ = Path(__file__).parents[3]
SNAPSHOTS = RAIZ / "data" / "snapshots"


# Directorios que no se recorren durante este scanner.
# Esto evita recorridos innecesariamente pesados.
PESADAS = {
    ".git",
    "storage",
    "llama.cpp",
    ".cache",
    ".fonts",
    ".local",
    "node_modules",
    "__pycache__",
}


def espacio() -> dict[str, float]:
    """Obtiene información real del espacio del sistema de archivos."""

    st = os.statvfs(HOME)

    total = st.f_blocks * st.f_frsize
    libre = st.f_bavail * st.f_frsize
    usado = total - libre

    return {
        "total_gb": round(total / 1e9, 2),
        "usado_gb": round(usado / 1e9, 2),
        "libre_gb": round(libre / 1e9, 2),
    }


def _normalizar_zonas(
    zonas: Iterable[str],
) -> set[Path]:
    """Convierte las zonas protegidas en rutas absolutas."""

    resultado: set[Path] = set()

    for zona in zonas:
        try:
            ruta = Path(zona).expanduser()

            if not ruta.is_absolute():
                ruta = HOME / ruta

            resultado.add(
                ruta.resolve(strict=False)
            )

        except (OSError, RuntimeError, TypeError):
            continue

    return resultado


def _esta_protegida(
    ruta: Path,
    zonas: set[Path],
) -> bool:
    """Determina si una ruta está dentro de una zona protegida."""

    try:
        ruta = ruta.resolve(strict=False)

    except (OSError, RuntimeError):
        # Ante una ruta que no podemos resolver con seguridad,
        # se considera protegida.
        return True

    for zona in zonas:
        try:
            ruta.relative_to(zona)
            return True

        except ValueError:
            continue

    return False


def _confianza_archivo_grande(
    tamano_bytes: int,
) -> float:
    """Estima confianza de que un archivo merezca revisión.

    La confianza se basa únicamente en el tamaño.

    No representa certeza de que el archivo deba eliminarse.
    """

    gb = tamano_bytes / 1e9

    if gb >= 10:
        return 0.97

    if gb >= 5:
        return 0.94

    if gb >= 2:
        return 0.90

    if gb >= 1:
        return 0.87

    if gb >= 0.5:
        return 0.80

    return 0.70


def _mostrar_progreso(
    cont: int,
    hallazgos: int,
    protegidos: int,
    omitidos: int,
) -> None:
    """Muestra telemetría compacta del escaneo."""

    mensaje = (
        f"\r\033[2K"
        f"   🔬 {cont:,} archivos"
        f" │ 🔎 {hallazgos:,} hallazgos"
        f" │ 🛡️ {protegidos:,} protegidos"
        f" │ ⏭️ {omitidos:,} omitidos"
    )

    print(
        mensaje,
        end="",
        flush=True,
    )


def archivos_grandes(
    zonas: Iterable[str],
    ext_crit: Iterable[str],
    top: int = 10,
    minimo_mb: int = 10,
) -> list[dict[str, Any]]:
    """Encuentra archivos grandes.

    Mantiene el formato histórico:

        [
            {
                "mb": 123.4,
                "ruta": "/ruta/archivo"
            }
        ]

    No modifica ningún archivo.
    """

    hallazgos: list[tuple[int, str]] = []

    cont = 0
    protegidos = 0
    omitidos = 0

    zonas_normalizadas = _normalizar_zonas(zonas)

    extensiones_criticas = {
        str(extension).lower()
        for extension in ext_crit
    }

    print()
    print("   🔬 Iniciando recorrido...")
    print()

    try:
        for raiz, dirs, files in os.walk(HOME):

            raiz_path = Path(raiz)

            # Evitar directorios pesados y protegidos.
            dirs_filtradas: list[str] = []

            for directorio in dirs:

                ruta_directorio = (
                    raiz_path / directorio
                )

                if directorio in PESADAS:
                    omitidos += 1
                    continue

                if _esta_protegida(
                    ruta_directorio,
                    zonas_normalizadas,
                ):
                    protegidos += 1
                    continue

                dirs_filtradas.append(directorio)

            dirs[:] = dirs_filtradas

            for nombre in files:

                cont += 1

                ruta = raiz_path / nombre

                if _esta_protegida(
                    ruta,
                    zonas_normalizadas,
                ):
                    protegidos += 1

                    if cont % 250 == 0:
                        _mostrar_progreso(
                            cont,
                            len(hallazgos),
                            protegidos,
                            omitidos,
                        )

                    continue

                if (
                    ruta.suffix.lower()
                    in extensiones_criticas
                ):
                    omitidos += 1

                    if cont % 250 == 0:
                        _mostrar_progreso(
                            cont,
                            len(hallazgos),
                            protegidos,
                            omitidos,
                        )

                    continue

                try:
                    tamano = ruta.stat().st_size

                except OSError:
                    omitidos += 1

                    if cont % 250 == 0:
                        _mostrar_progreso(
                            cont,
                            len(hallazgos),
                            protegidos,
                            omitidos,
                        )

                    continue

                if tamano >= minimo_mb * 1024 * 1024:
                    hallazgos.append(
                        (
                            tamano,
                            str(ruta),
                        )
                    )

                if cont % 250 == 0:
                    _mostrar_progreso(
                        cont,
                        len(hallazgos),
                        protegidos,
                        omitidos,
                    )

    except OSError:
        # El scanner es observacional. Si el recorrido falla,
        # conserva los hallazgos obtenidos hasta ese momento.
        pass

    # Limpiar la línea de progreso.
    print(
        "\r\033[2K",
        end="",
    )

    print(
        f"   ✓ {cont:,} archivos analizados"
        f" │ 🔎 {len(hallazgos):,} hallazgos"
        f" │ 🛡️ {protegidos:,} protegidos"
        f" │ ⏭️ {omitidos:,} omitidos"
    )

    hallazgos.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        {
            "mb": round(
                tamano / 1e6,
                1,
            ),
            "ruta": ruta,
        }
        for tamano, ruta in hallazgos[:top]
    ]


def generar_evidencias_archivos_grandes(
    hallazgos: list[dict[str, Any]],
    *,
    sequence_start: int = 1,
    snapshot_id: str | None = None,
) -> list[Evidence]:
    """Convierte hallazgos tradicionales en Evidence.

    Solamente observa y estructura información.

    No ejecuta ninguna acción.
    """

    evidencias: list[Evidence] = []

    for offset, hallazgo in enumerate(hallazgos):

        try:
            ruta = Path(
                hallazgo["ruta"]
            )

        except (KeyError, TypeError):
            continue

        try:
            evidence = evidence_from_file(
                sequence=sequence_start + offset,
                path=ruta,
                source=EvidenceSource.STORAGE_SCANNER,
                category=EvidenceCategory.REVIEW,
                calculate_hash=False,
                snapshot_id=snapshot_id,
            )

        except (OSError, ValueError):
            continue

        confidence = _confianza_archivo_grande(
            evidence.size_bytes or 0
        )

        evidence.confidence = confidence

        evidence.add_reason(
            "large_file",
            (
                "El archivo supera el umbral configurado "
                "para archivos grandes."
            ),
        )

        evidence.recommendation = (
            "Revisar si el archivo sigue siendo necesario. "
            "No se recomienda ninguna acción automática."
        )

        evidencias.append(
            evidence
        )

    return evidencias


def _siguiente_sequence(
    snapshot_id: str | None = None,
) -> int:
    """Obtiene una secuencia segura para Snapshot.

    Actualmente utiliza los snapshots existentes para intentar
    continuar la numeración BLUMCL-S-XXXXXX.

    Si no puede determinarse una secuencia, comienza en 1.

    Esta función solamente inspecciona archivos de snapshot.
    """

    max_sequence = 0

    if not SNAPSHOTS.exists():
        return 1

    try:
        for archivo in SNAPSHOTS.glob("*.json"):

            try:
                datos = json.loads(
                    archivo.read_text(
                        encoding="utf-8"
                    )
                )

            except (
                OSError,
                UnicodeDecodeError,
                json.JSONDecodeError,
            ):
                continue

            identificador = datos.get(
                "snapshot_id"
            )

            if not isinstance(
                identificador,
                str,
            ):
                continue

            prefijo = "BLUMCL-S-"

            if not identificador.startswith(
                prefijo
            ):
                continue

            numero = identificador[
                len(prefijo):
            ]

            if numero.isdigit():
                max_sequence = max(
                    max_sequence,
                    int(numero),
                )

    except OSError:
        return 1

    return max_sequence + 1


def crear_snapshot(
    *,
    hallazgos: list[dict[str, Any]],
    evidencias: list[Evidence],
    sequence: int | None = None,
    metadata: dict[str, Any] | None = None,
) -> Snapshot:
    """Construye el Snapshot oficial de BLUMCL.

    Este es el nuevo camino arquitectónico:

        hallazgos
            ↓
        Evidence
            ↓
        Snapshot.create()
            ↓
        SnapshotFile
        Evidence
            ↓
        Snapshot

    No modifica ningún archivo analizado.
    """

    datos_espacio = espacio()

    if sequence is None:
        sequence = _siguiente_sequence()

    total_bytes = int(
        datos_espacio["total_gb"] * 1e9
    )

    used_bytes = int(
        datos_espacio["usado_gb"] * 1e9
    )

    free_bytes = int(
        datos_espacio["libre_gb"] * 1e9
    )

    snapshot = Snapshot.create(
        sequence=sequence,
        total_bytes=total_bytes,
        used_bytes=used_bytes,
        free_bytes=free_bytes,
        metadata={
            "scanner": "storage",
            "scanner_version": "2.2",
            "home": str(HOME),
            "hallazgos_count": len(
                hallazgos
            ),
            **(metadata or {}),
        },
    )

    # Registrar los archivos observados.
    for hallazgo in hallazgos:

        try:
            ruta = Path(
                hallazgo["ruta"]
            )

        except (KeyError, TypeError):
            continue

        try:
            stat = ruta.stat()

        except OSError:
            continue

        snapshot.add_file(
            path=str(ruta),
            size_bytes=stat.st_size,
        )

    # Registrar evidencia asociada.
    for evidence in evidencias:

        # Evidence puede venir ya asociado a un snapshot
        # histórico. En ese caso no podemos reasignarlo
        # silenciosamente.
        if evidence.snapshot_id is None:
            evidence.snapshot_id = (
                snapshot.snapshot_id
            )

        if (
            evidence.snapshot_id
            != snapshot.snapshot_id
        ):
            # No asociamos silenciosamente evidencia de otro
            # snapshot.
            continue

        snapshot.add_evidence(
            evidence
        )

    return snapshot


def analizar_snapshot(
    *,
    sequence: int | None = None,
) -> Snapshot:
    """Ejecuta el scanner y devuelve el Snapshot oficial.

    Esta es la nueva API recomendada para código nuevo.

    ``analizar()`` permanece disponible para compatibilidad.
    """

    cfg = cargar()

    zonas = cfg.get(
        "zonas_intocables",
        [],
    )

    extensiones = {
        str(extension).lower()
        for extension in cfg.get(
            "extensiones_criticas",
            [],
        )
    }

    minimo_mb = int(
        cfg.get(
            "tamano_grande_mb",
            10,
        )
    )

    hallazgos = archivos_grandes(
        zonas,
        extensiones,
        minimo_mb=minimo_mb,
    )

    evidencias = generar_evidencias_archivos_grandes(
        hallazgos,
        sequence_start=1,
        snapshot_id=None,
    )

    return crear_snapshot(
        hallazgos=hallazgos,
        evidencias=evidencias,
        sequence=sequence,
        metadata={
            "threshold_mb": minimo_mb,
            "protected_zones": [
                str(zona)
                for zona in zonas
            ],
            "critical_extensions": sorted(
                extensiones
            ),
        },
    )


def analizar() -> dict[str, Any]:
    """Ejecuta un análisis de almacenamiento.

    Mantiene las claves históricas:

        fecha
        snapshot_id
        espacio
        archivos_grandes
        evidencias

    Internamente utiliza ahora el Snapshot oficial.

    Esto permite migrar progresivamente el proyecto sin romper
    el código existente.
    """

    fecha = datetime.now(
        timezone.utc
    ).isoformat()

    snapshot = analizar_snapshot()

    return {
        "fecha": fecha,
        "snapshot_id": snapshot.snapshot_id,
        "espacio": espacio(),
        "archivos_grandes": [
            {
                "mb": round(
                    file_data.size_bytes / 1e6,
                    1,
                ),
                "ruta": file_data.path,
            }
            for file_data in snapshot.files
        ],
        "evidencias": [
            evidence.to_dict()
            for evidence in snapshot.evidences
        ],
        "snapshot": snapshot.to_dict(),
    }


def guardar_snapshot(
    datos: dict[str, Any],
) -> Path:
    """Guarda un snapshot en JSON.

    Compatibilidad histórica.

    El sistema nuevo debe preferir:

        Snapshot.to_json()

    y utilizar esta función solamente cuando una parte antigua
    del proyecto todavía espere un diccionario.
    """

    SNAPSHOTS.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    nombre = f"{timestamp}.json"

    ruta = SNAPSHOTS / nombre

    ruta.write_text(
        json.dumps(
            datos,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return ruta


def guardar_snapshot_oficial(
    snapshot: Snapshot,
) -> Path:
    """Guarda un Snapshot oficial de BLUMCL.

    Utiliza Snapshot.to_json() en lugar de construir
    manualmente el JSON.
    """

    SNAPSHOTS.mkdir(
        parents=True,
        exist_ok=True,
    )

    ruta = (
        SNAPSHOTS
        / f"{snapshot.snapshot_id}.json"
    )

    ruta.write_text(
        snapshot.to_json(),
        encoding="utf-8",
    )

    return ruta


def autodiagnostico() -> list[str]:
    """Genera avisos informativos sin ejecutar acciones."""

    avisos: list[str] = []

    build = HOME / "llama.cpp" / "build"

    if build.exists():
        avisos.append(
            "~/llama.cpp/build existe: si ya usas "
            "llama-cpp por pkg, puedes revisarla para "
            "determinar si sigue siendo necesaria."
        )

    for modelo in (
        "qwen25-15b.gguf",
        "llama32.gguf",
        "qwen3.gguf",
    ):

        path = HOME / modelo

        if not path.exists():
            continue

        try:
            size_mb = round(
                path.stat().st_size / 1e6
            )

        except OSError:
            continue

        avisos.append(
            f"{modelo}: {size_mb} MB "
            "(modelo de IA: conservar si se utiliza)."
        )

    return avisos


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
