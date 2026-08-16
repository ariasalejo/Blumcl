"""BLUMCL · CAPA PREMIUM · post-acciones automáticas.
Solo lectura · nunca rompe · reutiliza snapshots."""
import json, time
from pathlib import Path

def _ok(m): print(f"\033[92m✅ {m}\033[0m")
def _warn(m): print(f"\033[93m⚠️  {m}\033[0m")
def _info(m): print(f"\033[96mℹ️  {m}\033[0m")
def _gem(m): print(f"\033[1;97m💎 {m}\033[0m")

def _banner():
    print()
    print("\033[1m✨ CAPA PREMIUM · AUTOMÁTICA\033[0m")
    print("─" * 56)

def _num(v):
    try: return float(v)
    except Exception: return 0.0

def _hum(b):
    b = _num(b)
    for u in ("B", "KB", "MB", "GB"):
        if b < 1024: return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} TB"

def _snap_dir():
    for c in (Path("snapshots"), Path.home()/"Blumcl"/"snapshots",
              Path("data")/"history"):
        if c.exists() and any(c.glob("*.json")):
            return c
    return None

def _cargar_snaps(n=2):
    d = _snap_dir()
    if not d: return []
    out = []
    for p in sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime)[-n:]:
        try: out.append(json.loads(p.read_text()))
        except Exception: continue
    return out

def _iter_archivos(snap):
    datos = snap
    if isinstance(snap, dict):
        datos = None
        for k in ("archivos", "files", "indice", "index", "entries"):
            if isinstance(snap.get(k), list):
                datos = snap[k]; break
        if datos is None: return
    if not isinstance(datos, list): return
    for e in datos:
        if not isinstance(e, dict): continue
        tgt = e.get("target") if isinstance(e.get("target"), dict) else {}
        ruta = e.get("ruta") or e.get("path") or tgt.get("path")
        if ruta:
            yield (str(ruta),
                   _num(e.get("tamano") or e.get("size") or tgt.get("size")),
                   _num(e.get("mtime") or e.get("modificado")))
