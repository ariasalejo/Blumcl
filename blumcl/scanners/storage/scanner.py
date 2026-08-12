"""Blumcl · scanner de almacenamiento.

Regla 1: observar sin modificar.
v2: modo rápido (salta directorios pesados) y progreso en vivo.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from blumcl.utils.config import cargar

HOME = Path.home()
RAIZ = Path(__file__).parents[3]
SNAPSHOTS = RAIZ / "data" / "snapshots"

PESADAS = {".git", "storage", "llama.cpp", ".cache", ".fonts",
           ".local", "node_modules", "__pycache__"}


def espacio():
    st = os.statvfs(HOME)
    total = st.f_blocks * st.f_frsize
    libre = st.f_bavail * st.f_frsize
    return {
        "total_gb": round(total / 1e9, 2),
        "usado_gb": round((total - libre) / 1e9, 2),
        "libre_gb": round(libre / 1e9, 2),
    }


def archivos_grandes(zonas, ext_crit, top=10, minimo_mb=10):
    hallazgos = []
    cont = 0
    for raiz, dirs, files in os.walk(HOME):
        dirs[:] = [d for d in dirs
                   if d not in zonas and d not in PESADAS]
        for nombre in files:
            cont += 1
            if cont % 800 == 0:
                print(".", end="", flush=True)
            ruta = Path(raiz) / nombre
            if nombre in zonas or ruta.suffix in ext_crit:
                continue
            try:
                tam = ruta.stat().st_size
            except OSError:
                continue
            if tam >= minimo_mb * 1024 * 1024:
                hallazgos.append((tam, str(ruta)))
    print(f" ({cont} archivos leídos)")
    hallazgos.sort(reverse=True)
    return [{"mb": round(t / 1e6, 1), "ruta": r} for t, r in hallazgos[:top]]


def analizar():
    cfg = cargar()
    return {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "espacio": espacio(),
        "archivos_grandes": archivos_grandes(
            set(cfg.get("zonas_intocables", [])),
            set(cfg.get("extensiones_criticas", [])),
        ),
    }


def guardar_snapshot(datos):
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    nombre = datetime.now().strftime("%Y-%m-%d_%H-%M") + ".json"
    ruta = SNAPSHOTS / nombre
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2))
    return ruta


def autodiagnostico():
    avisos = []
    build = HOME / "llama.cpp" / "build"
    if build.exists():
        avisos.append("~/llama.cpp/build existe: si ya usas llama-cpp "
                      "por pkg, puedes borrarla y liberar espacio.")
    for modelo in ["qwen25-15b.gguf", "llama32.gguf", "qwen3.gguf"]:
        p = HOME / modelo
        if p.exists():
            avisos.append(f"{modelo}: {round(p.stat().st_size / 1e6)} MB "
                          "(modelo de IA: conservar si lo usas).")
    return avisos
