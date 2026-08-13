"""Blumcl · configuración con valores predeterminados seguros.

Si el archivo no existe, está vacío o está corrupto,
Blumcl lo regenera automáticamente.
"""

import json
from pathlib import Path


RUTA = Path(__file__).parents[2] / "config" / "proteccion.json"

DEFAULTS = {
    "zonas_intocables": [
        ".ssh",
        ".termux",
        ".gnupg",
        ".config",
    ],
    "extensiones_criticas": [
        ".key",
        ".pem",
        ".gpg",
        ".keystore",
    ],
    "tamano_grande_mb": 100,
}


def _guardar_predeterminados():
    """Regenera la configuración segura predeterminada."""
    RUTA.parent.mkdir(parents=True, exist_ok=True)
    RUTA.write_text(
        json.dumps(DEFAULTS, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def cargar():
    """Carga la configuración o regenera los valores predeterminados."""
    if not RUTA.exists():
        _guardar_predeterminados()
        return dict(DEFAULTS)

    try:
        contenido = RUTA.read_text(encoding="utf-8").strip()

        if not contenido:
            _guardar_predeterminados()
            return dict(DEFAULTS)

        datos = json.loads(contenido)

        if not isinstance(datos, dict):
            _guardar_predeterminados()
            return dict(DEFAULTS)

        return datos

    except (json.JSONDecodeError, OSError, TypeError):
        _guardar_predeterminados()
        return dict(DEFAULTS)


def guardar(cfg):
    """Guarda una configuración válida."""
    RUTA.parent.mkdir(parents=True, exist_ok=True)

    RUTA.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
