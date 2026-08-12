"""Blumcl · aprendizaje simple: recuerda decisiones y sugiere."""

import json
from pathlib import Path

RUTA = Path(__file__).parents[2] / "data" / "history" / "preferencias.json"


def _cargar():
    if RUTA.exists():
        try:
            return json.loads(RUTA.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def registrar(evento, ruta):
    mem = _cargar()
    clave = str(ruta)
    mem.setdefault(clave, {"cancelo": 0, "protegio": 0})
    mem[clave][evento] = mem[clave].get(evento, 0) + 1
    RUTA.parent.mkdir(parents=True, exist_ok=True)
    RUTA.write_text(json.dumps(mem, ensure_ascii=False, indent=2))


def sugerencias():
    return [r for r, ev in _cargar().items() if ev.get("cancelo", 0) >= 2]
