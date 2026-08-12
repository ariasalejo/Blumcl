"""Blumcl · configuración con defaults seguros.

Si el archivo no existe o está corrupto, se regenera solo.
"""

import json
from pathlib import Path

RUTA = Path(__file__).parents[2] / "config" / "proteccion.json"

DEFAULTS = {
    "zonas_intocables": [".ssh", ".termux", ".gnupg", ".config"],
    "extensiones_criticas": [".key", ".pem", ".gpg", ".keystore"],
    "tamano_grande_mb": 100,
}


def cargar():
    if not RUTA.exists():
        RUTA.parent.mkdir(parents=True, exist_ok=True)
        RUTA.write_text(json.dumps(DEFAULTS, ensure_ascii=False, indent=2))
        return dict(DEFAULTS)
    try:
        return json.loads(RUTA.read_text())
    except json.JSONDecodeError:
        return dict(DEFAULTS)


def guardar(cfg):
    RUTA.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))
