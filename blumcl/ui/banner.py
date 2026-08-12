"""Blumcl · banner responsivo + frases de seguridad."""

import os
import re
import random
from unicodedata import east_asian_width as _ew

FRASES = [
    "La seguridad es un proceso, no un producto",
    "Confía, pero verifica",
    "Observa antes de actuar",
    "Tus datos, tu decisión",
    "Primero conservar, luego actuar",
    "Piensa antes de hacer clic",
    "El eslabón más fuerte eres tú",
]


def _dw(s):
    sin = re.sub(r"\x1b\[[0-9;]*m", "", s)
    return sum(2 if _ew(c) in "WF" else 1 for c in sin)


def ancho_terminal():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 44


def frase_seguridad(w, animar=True):
    import time
    f = random.choice(FRASES)
    espaciada = " ".join(f)
    if _dw(espaciada) > w - 4:
        espaciada = f
    pad = max(0, (w - _dw(espaciada)) // 2)
    am, gris, r = "\033[1;93m", "\033[90m", "\033[0m"
    if animar and pad > 3:
        paso = max(1, pad // 10)
        for q in range(0, pad, paso):
            print(f"\033[2K\r{am}{' ' * q}{espaciada}{r}", end="", flush=True)
            time.sleep(0.03)
    print(f"\033[2K\r{am}{' ' * pad}{espaciada}{r}")
    print(f"{gris}{' ' * (pad + 2)}{espaciada}{r}")


def cabecera(disco_str, version, color=True):
    w = max(44, min(ancho_terminal(), 80))
    c = "\033[96m" if color else ""
    b = "\033[1m" if color else ""
    r = "\033[0m" if color else ""

    def linea(texto):
        dw = _dw(texto)
        esp = max(0, (w - 2 - dw)) // 2
        contenido = " " * esp + texto
        contenido += " " * max(0, w - 2 - dw - esp)
        return f"{c}║ {contenido} ║{r}"

    titulo = f"{b}🚀  B L U M C L  v{version}{r}"
    sub = "Observar · Analizar · Confirmar · Actuar"

    return "\n".join([
        f"{c}╔{'═' * (w - 2)}╗{r}",
        linea(titulo),
        linea(sub),
        f"{c}╠{'═' * (w - 2)}╣{r}",
        linea(disco_str),
        f"{c}╚{'═' * (w - 2)}╝{r}",
    ])
