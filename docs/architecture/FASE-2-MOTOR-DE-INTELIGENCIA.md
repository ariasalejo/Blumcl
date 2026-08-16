blumcl/scanners/storage/__init__.py está vacío.
Eso explica por qué en workflows tienes:
_carga("storage", "blumcl.scanners.storage")
pero después intentas resolver:
("StorageScanner", "Scanner")
y no existe ninguna de esas clases expuesta por el paquete. En realidad tu scanner actual funciona como módulo funcional con:
analizar()
archivos_grandes()
espacio()
Así que no vamos a romper lo que ya funciona. Vamos a adaptar la arquitectura a lo que realmente tienes.
🧭 FASE 2 que vamos a construir
La dejaría así:
FASE 2 · MOTOR DE INTELIGENCIA BLUMCL
│
├── 2.1 Contrato del Scanner
│     └── definir qué debe devolver cualquier scanner
│
├── 2.2 Integrar Snapshot real
│     └── usar blumcl/core/snapshot.py
│
├── 2.3 Separar Evidence de Finding
│     ├── Evidence = hecho observado
│     └── Finding  = interpretación
│
├── 2.4 Intelligence Engine
│     └── convierte evidencia → hallazgos
│
├── 2.5 Scoring
│     └── calcula prioridad/riesgo
│
├── 2.6 Signals
│     └── detecta patrones importantes
│
└── 2.7 Opción 1
      └── Scanner
          ↓
        Snapshot
          ↓
        Evidence
          ↓
        Findings
          ↓
        Signals
          ↓
        Score
          ↓
        Decisión sugerida
Y hay algo que quiero conservar de lo que ya construimos:
BLUMCL observa primero y actúa después.
Nada de este motor debe borrar archivos.
2.1 · CONTRATO DEL SCANNER
Primero vamos a establecer el contrato.
Tu scanner de almacenamiento actualmente produce:
{
    "fecha": ...,
    "snapshot_id": ...,
    "espacio": ...,
    "archivos_grandes": ...,
    "evidencias": ...
}
Eso está bien, pero cada scanner debería entregar una estructura común.
Vamos a crear:
blumcl/core/scanner_contract.py
Ponlo con nano:
nano blumcl/core/scanner_contract.py
Y pega:
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
Guarda:
CTRL + O
ENTER
CTRL + X
2.2 · PRIMERA CORRECCIÓN IMPORTANTE
Ahora vamos a hacer que storage exponga correctamente su scanner.
Actualmente:
cat blumcl/scanners/storage/__init__.py
te devuelve vacío.
Eso lo vamos a cambiar.
nano blumcl/scanners/storage/__init__.py
Pon:
"""
BLUMCL · Storage Scanner
"""

from .scanner import (
    analizar,
    archivos_grandes,
    autodiagnostico,
    espacio,
    generar_evidencias_archivos_grandes,
    guardar_snapshot,
)

__all__ = [
    "analizar",
    "archivos_grandes",
    "autodiagnostico",
    "espacio",
    "generar_evidencias_archivos_grandes",
    "guardar_snapshot",
]
Esto es importante porque ahora:
import blumcl.scanners.storage
sí tendrá disponibles las funciones reales.
⚠️ Pero aquí hay otra cosa
Tu workflows está buscando esto:
("StorageScanner", "Scanner")
y nosotros no tenemos esas clases.
Por ahora no vamos a inventar una clase solamente para satisfacer el workflow.
Vamos a hacer que el workflow entienda el scanner funcional existente.
Es decir:
ANTES

workflow
   ↓
StorageScanner
   ↓
scan()


AHORA

workflow
   ↓
analizar()
   ↓
ScanResult
Eso es mucho más limpio para el código que ya tienes.
2.3 · SNAPSHOT REAL
Aquí tenemos una buena noticia.
Ya existe:
blumcl/core/snapshot.py
y además encontramos:
Snapshot.create()
Así que no debemos seguir creando snapshots con JSON manuales desde el scanner como arquitectura principal.
Tu función actual:
def guardar_snapshot(datos: dict) -> Path:
puede quedarse temporalmente por compatibilidad histórica.
Pero la arquitectura nueva será:
Scanner
   ↓
ScanResult
   ↓
Snapshot.create()
   ↓
Snapshot.add_file()
Snapshot.add_evidence()
   ↓
Snapshot.to_json()
Eso nos permitirá posteriormente hacer:
Snapshot A
      ↓
Snapshot B
      ↓
Comparador
      ↓
cambios
que es exactamente lo que queremos para BLUMCL.
2.4 · Evidence vs Finding
Esta es probablemente la mejora conceptual más importante de toda la FASE 2.
Ahora mismo tienes Evidence.
Por ejemplo:
archivo:
qwen3.gguf

tamaño:
4.2 GB

ruta:
~/qwen3.gguf
Eso es un hecho.
BLUMCL no debería decir inmediatamente:
"BORRAR"
Debe decir:
EVIDENCE
   ↓
archivo de 4.2 GB
   ↓
ubicado en HOME
   ↓
modelo GGUF
Después otro componente interpreta:
FINDING

"Se detectó un modelo de IA local de gran tamaño.
Puede ser relevante para el usuario.
No se recomienda eliminar automáticamente."
Entonces:
Evidence = LO QUE SABEMOS

Finding = LO QUE INTERPRETAMOS

Signal = PATRÓN QUE DETECTAMOS

Score = PRIORIDAD QUE CALCULAMOS

Recommendation = QUÉ CONVIENE CONSIDERAR
Esta separación va a hacer que Blumcl se sienta muchísimo más profesional.
2.5 · Intelligence Engine
Después crearemos:
blumcl/intelligence/
├── __init__.py
├── engine.py
├── finding.py
├── scoring.py
└── signals.py
Y el flujo será:
                    BLUMCL
                       │
                       ▼
                 ┌───────────┐
                 │  SCANNER  │
                 └─────┬─────┘
                       │
                       ▼
                 ┌───────────┐
                 │  EVIDENCE │
                 └─────┬─────┘
                       │
                       ▼
               ┌────────────────┐
               │ INTELLIGENCE   │
               │ ENGINE         │
               └───────┬────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Findings      Signals       Score
          │            │            │
          └────────────┼────────────┘
                       ▼
                RECOMENDACIÓN
2.6 · Signals
Aquí podremos empezar a darle verdadera inteligencia a Blumcl.
Por ejemplo:
SIGNAL: LARGE_FILE

archivo > umbral
SIGNAL: AI_MODEL

extensión .gguf
SIGNAL: PROTECTED_PATH

archivo dentro de zona protegida
SIGNAL: STORAGE_PRESSURE

poco espacio libre
Y posteriormente:
SIGNAL: DUPLICATE
SIGNAL: CACHE_PRESSURE
SIGNAL: OLD_ARTIFACT
SIGNAL: TEMPORARY_ARTIFACT
SIGNAL: LARGE_LOG
SIGNAL: BUILD_ARTIFACT
Ahí BLUMCL empieza a pasar de:
"te muestro archivos grandes"
a:
"entiendo qué clase de situación estoy observando".
2.7 · SCORING
Después podemos tener algo como:
                     PRIORIDAD

                     0 ───────── 100

0-20       🟢 informativo
21-40      🔵 bajo
41-60      🟡 moderado
61-80      🟠 alto
81-100     🔴 crítico
Pero ojo:
el score no significa:
"hay que borrar".
Significa:
"esto merece atención".
Ejemplo:
qwen3.gguf
──────────────
4.2 GB
modelo IA
usuario podría necesitarlo

Impacto:       70
Confianza:     97
Acción:        NONE

PRIORIDAD:     35
Aunque sea enorme, no necesariamente es peligroso.
Eso es inteligencia contextual.
🔥 Y finalmente opción 1
Tu actual:
1. ESCANEAR
dejará de hacer simplemente:
Storage
CPU
RAM
Snapshot
Resumen
y evolucionará hacia:
🔬 ESCANEAR SISTEMA
        │
        ├── Storage
        ├── CPU
        └── RAM
              │
              ▼
        NORMALIZACIÓN
              │
              ▼
           SNAPSHOT
              │
              ▼
           EVIDENCE
              │
              ▼
        INTELLIGENCE ENGINE
              │
       ┌──────┼───────┐
       ▼      ▼       ▼
    FINDING SIGNAL  SCORE
       │      │       │
       └──────┼───────┘
              ▼
       📋 RESUMEN
              │
              ▼
       🎯 SIGUIENTE PASO
Y esto encaja perfectamente con la filosofía que hemos venido construyendo:
entender → diseñar → verificar → decidir
🛑 Pero no avancemos todavía con los 7 módulos
Quiero que lo hagamos de ingeniería real, no pegar 2.000 líneas y después perseguir errores.
Ahora solo hagamos 2.1
Ejecuta exactamente:
nano blumcl/core/scanner_contract.py
pega el archivo que te dejé arriba, guarda y luego:
nano blumcl/scanners/storage/__init__.py
pega el segundo archivo.
Después prueba:
python - <<'PY'
import blumcl.scanners.storage as storage

print("STORAGE OK")
print("analizar:", callable(storage.analizar))
print("espacio:", callable(storage.espacio))
print("archivos_grandes:", callable(storage.archivos_grandes))
PY
No toques todavía workflows/__init__.py.
Primero quiero que consigamos:
STORAGE OK
analizar: True
espacio: True
archivos_grandes: True
Cuando eso pase, nos vamos a 2.2 — conectar Snapshot.create() real con el scanner, y ahí sí vamos a aprovechar el snapshot.py que ya tienes en vez de construir otro sistema paralelo.
