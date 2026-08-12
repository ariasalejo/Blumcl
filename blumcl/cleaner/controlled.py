"""Blumcl · limpieza controlada: cuarentena y confirmación."""

import shutil
import time
from pathlib import Path


def plan():
    home = Path.home()
    candidatos = [home / "llama.cpp" / "build",
                  home / ".cache",
                  home / "kali_instalar"]
    return [str(p) for p in candidatos if p.exists()]


def cuarentena(ruta):
    """Mueve a ~/blumcl_papelera con marca de tiempo. Nunca rm -rf."""
    raiz = Path.home() / "blumcl_papelera"
    raiz.mkdir(exist_ok=True)
    nombre = Path(ruta).name + "_" + time.strftime("%Y%m%d_%H%M")
    destino = raiz / nombre
    shutil.move(str(ruta), str(destino))
    return destino
